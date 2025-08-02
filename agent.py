"""
AI agent implementation for Synapse Trader.
Handles communication with Anthropic Claude and orchestrates tool usage.
"""

from __future__ import annotations

import json
import os
import re
from typing import List, Dict, Any

from dotenv import load_dotenv
import anthropic

# Load env vars early so they are available during module import
load_dotenv()

from tools import (
    price_fx_forward,
    check_limits,
    record_audit,
    log_audit_event,
)

# ---------------------------------------------------------------------------
# ACI.dev setup
# ---------------------------------------------------------------------------
from aci import ACI, to_json_schema  # type: ignore
from aci.types.enums import FunctionDefinitionFormat

ACI_API_KEY = os.getenv("ACI_API_KEY")
if not ACI_API_KEY:
    raise RuntimeError("ACI_API_KEY missing in environment")

aci = ACI(api_key=ACI_API_KEY)

# ---------------------------------------------------------------------------
# ACI-compatible tool schemas for our local Python functions
# ---------------------------------------------------------------------------
CUSTOM_TOOL_SCHEMAS = [
    {
        "type": "custom",
        "function": {
            "name": "price_fx_forward",
            "description": "Return FX-forward price & forward points",
            "parameters": {
                "type": "object",
                "properties": {
                    "ccy_pair": {"type": "string", "description": "Currency pair (e.g. 'GBPUSD')"},
                    "spot_rate": {"type": "number", "description": "Current spot FX rate"},
                    "usd_rate": {"type": "number", "description": "3-month USD interest rate"},
                    "gbp_rate": {"type": "number", "description": "3-month GBP interest rate"}
                },
                "required": ["ccy_pair", "spot_rate", "usd_rate", "gbp_rate"]
            }
        }
    },
    {
        "type": "custom",
        "function": {
            "name": "check_limits",
            "description": "Check client credit limits",
            "parameters": {
                "type": "object",
                "properties": {
                    "client_id": {"type": "string", "description": "Client identifier"},
                    "notional_usd": {"type": "number", "description": "Trade size in USD"}
                },
                "required": ["client_id", "notional_usd"]
            }
        }
    },
    {
        "type": "custom",
        "function": {
            "name": "record_audit",
            "description": "Book trade and return transaction id",
            "parameters": {
                "type": "object",
                "properties": {
                    "trade_json": {
                        "type": "object",
                        "description": "Complete trade details as JSON"
                    }
                },
                "required": ["trade_json"]
            }
        }
    }
]


# ---------------------------------------------------------------------------
# Anthropic client initialisation
# ---------------------------------------------------------------------------

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY not found in environment. Did you set up your .env file?")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# ---------------------------------------------------------------------------
# System prompt – this controls the behaviour of the agent.
# Keep it concise for now; refine during demo iterations.
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    """You are SynapseTrader – a voice-enabled co-pilot for FX forward traders. \n"
    "You know about:\n        • USD/GBP 3-month FX forwards (and you only handle this product).\n"
    "Mission: quote, negotiate and book trades in a compliant manner.\n"
    "You have access to these tools:\n"
    "1. price_fx_forward – returns all-in forward price and forward points.\n"
    "   Signature: {\"name\": \"price_fx_forward\", \"args\": {\"ccy_pair\": \"USDGBP\", \"notional_usd\": 25000000, \"tenor\": \"3M\"}}\n"
    "2. check_limits – verifies client limits.\n"
    "   Signature: {\"name\": \"check_limits\", \"args\": {\"client_id\": \"ClientCorp\", \"notional_usd\": 25000000, \"tenor\": \"3M\"}}\n"
    "3. record_audit – books the trade and stores it.\n"
    "   Signature: {\"name\": \"record_audit\", \"args\": {\"trade_json\": {…}}}\n\n"
    "When you need one of these tools, respond ONLY with a JSON block inside \n"
    "triple-backtick fences (```json … ```). The JSON must have the keys \"name\" and \"args\". \n"
    "After you receive the <tool_result>, decide whether another tool call is \n"
    "needed or respond normally to the trader. Do not reference implementation details."""
)

# ---------------------------------------------------------------------------
# Tool mapping
# ---------------------------------------------------------------------------

TOOL_MAP = {
    "price_fx_forward": price_fx_forward,
    "check_limits": check_limits,
    "record_audit": record_audit,
}

# ---------------------------------------------------------------------------
# In-memory conversation history – this is reset on app restart.
# Streamlit keeps the agent module loaded across reruns, which is fine for the
# simple hackathon demo.
# ---------------------------------------------------------------------------

conversation_history: List[Dict[str, Any]] = []


# ---------------------------------------------------------------------------
# Conversation handling via ACI.dev – no manual function parsing needed
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

def _claude_chat() -> str:  # type: ignore[override]
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        system=SYSTEM_PROMPT,
        max_tokens=1024,
        messages=conversation_history,
        tools=CUSTOM_TOOL_SCHEMAS,
    )
    return response.content[0].text


# ---------------------------------------------------------------------------
# Conversation turn with tool execution
# ---------------------------------------------------------------------------

def _execute_tool_from_response(response_text: str) -> str | None:
    """If the assistant asked for a tool, execute it and return its result."""
    match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)
    if not match:
        return None

    try:
        tool_call = json.loads(match.group(1))
        tool_name: str = tool_call["name"]
        tool_args: Dict[str, Any] = tool_call.get("args", {})
    except (json.JSONDecodeError, KeyError) as err:
        return f"Error decoding tool request: {err}"

    tool_func = TOOL_MAP.get(tool_name)
    if tool_func is None:
        return f"Unknown tool requested: {tool_name}"

    try:
        tool_result = tool_func(**tool_args)
    except Exception as exc:
        tool_result = json.dumps({"status": "error", "error": str(exc)})

    return tool_result


def run_conversation_turn(user_message: str) -> str:
    """Handle one full turn including potential tool calls."""

    # 1. Append user message
    conversation_history.append({"role": "user", "content": user_message})

    # 2. First response from Claude
    assistant_response = _claude_chat()

    # 3. Check if a tool call is embedded
    tool_result = _execute_tool_from_response(assistant_response)
    if tool_result is None:
        # No tool needed – conversation turn finished.
        conversation_history.append({"role": "assistant", "content": assistant_response})
        return assistant_response.strip()

    # 4. Add assistant response + tool result to history
    conversation_history.append({"role": "assistant", "content": assistant_response})
    conversation_history.append({"role": "user", "content": f"<tool_result>\n{tool_result}\n</tool_result>"})

    # 5. Ask Claude to incorporate the tool result
    final_response = _claude_chat()

    conversation_history.append({"role": "assistant", "content": final_response})

    return final_response.strip()


# ---------------------------------------------------------------------------
# Public entry point used by the Streamlit front-end
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# New simpler run_conversation_turn using ACI
# ---------------------------------------------------------------------------

def run_conversation_turn(user_message: str) -> str:  # type: ignore[override]
    """Single chat turn – ACI handles function calling automatically."""
    conversation_history.append({"role": "user", "content": user_message})

    # --- get initial assistant response from Claude ---
    assistant_response = _claude_chat()

    # look for ```json tool call```
    match = re.search(r"```json\s*(.*?)\s*```", assistant_response, re.DOTALL)
    if not match:
        conversation_history.append({"role": "assistant", "content": assistant_response})
        return assistant_response.strip()

    tool_json = json.loads(match.group(1))
    tool_name = tool_json["name"]
    tool_args = tool_json.get("args", {})

    try:
        tool_result = aci.handle_function_call(tool_name, tool_args)
    except Exception as exc:
        tool_result = json.dumps({"status": "error", "error": str(exc)})

    # add both assistant response & tool result to history and ask Claude again
    conversation_history.append({"role": "assistant", "content": assistant_response})
    conversation_history.append({"role": "user", "content": f"<tool_result>\n{tool_result}\n</tool_result>"})

    final_response = _claude_chat()
    conversation_history.append({"role": "assistant", "content": final_response})
    return final_response.strip()

# ---------------------------------------------------------------------------

def process_user_input(user_message: str) -> str:
    """Wrapper to keep the original front-end function name."""
    try:
        reply = run_conversation_turn(user_message)
        return reply
    except Exception as exc:
        error_msg = f"Error processing request: {exc}"
        log_audit_event("error", {"error": error_msg})
        return error_msg
