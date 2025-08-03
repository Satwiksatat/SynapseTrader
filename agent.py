"""
AI agent implementation for Synapse Trader.
Handles conversation flow and tool orchestration.
"""

from dotenv import load_dotenv
load_dotenv()

import os
import json
import anthropic
import tools 
import tools
from inspect import signature, getdoc
from typing import Any
from elevenlabs.client import ElevenLabs

# Initialize clients
try:
    anthropic_client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
    eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
except KeyError as e:
    print(f"FATAL: {e} environment variable not set. Please set it to continue.")
    exit()

# --- Tool & Prompt Definition ---

AVAILABLE_TOOLS = {
    "get_market_data": tools.get_market_data,
    "check_credit_limit": tools.check_credit_limit,
    "check_trading_risk": tools.check_trading_risk,
    "get_desk_axe": tools.get_desk_axe,
    "record_trade_and_notify": tools.record_trade_and_notify,
}

SYSTEM_PROMPT = """
You are Synapse, an AI trading co-pilot. Your personality is professional, concise, and direct. Your mission is to assist a human trader to quote, negotiate, and book a plain-vanilla USD/GBP 3-month FX forward. All your responses must be in English.

You MUST use the provided tools to follow this exact workflow:

1.  **On a quote request:** You MUST perform all pre-trade checks first. This involves calling `check_credit_limit` for counterparty risk and `check_trading_risk` for internal desk risk. You must also call `get_desk_axe` to understand the desk's strategy.
2.  **Synthesize and Price:** After gathering pre-trade data, you MUST call `get_market_data` to get the mid-market price. Then, using all the pre-trade information, you will apply a strategic spread to the mid-market price to generate a final quote for the client. Briefly state your reasoning for the spread.
3.  **Negotiation:** The user may ask you to improve the price. You have the authority to improve the price once by a small, reasonable amount.
4.  **Booking:** When the user confirms the trade (e.g., "done", "book it"), you MUST call `record_trade_and_notify` to finalize the transaction, passing the final client, notional, and price.
5.  **Confirmation:** Provide a clear, final confirmation message including the transaction ID returned by the tool.
"""

def create_tool_spec(func) -> dict[str, Any]:
    """Creates a JSON tool specification from a Python function."""
    sig = signature(func)
    doc = getdoc(func)

    # A simple mapping from Python types to JSON schema types
    type_mapping = {str: "string", int: "number", float: "number", dict: "object"}

    params = {
        name: {"type": type_mapping.get(param.annotation, "string")}
        for name, param in sig.parameters.items()
    }

    return {
        "name": func.__name__,
        "description": doc.split('Args:')[0].strip() if doc else "",
        "input_schema": {
            "type": "object",
            "properties": params,
            "required": list(params.keys())
        }
    }

tools_spec = [create_tool_spec(func) for func in AVAILABLE_TOOLS.values()]

def process_user_input(user_input: str) -> str:
    """
    Process user input and return AI response.
    This is the main entry point for the Streamlit app.
    """
    conversation_history = [{"role": "user", "content": user_input}]
    history = run_conversation_turn(conversation_history)

    # Extract the final text response
    final_response = next(
        (block.text for block in history[-1]['content'] if hasattr(block, 'text')),
        "No text response found."
    )

    return final_response

def run_conversation_turn(history: list) -> list:
    """Runs one turn of the conversation, including multi-step tool use."""
    print(f"\nUser: {history[-1]['content']}")

    # Initial call to Claude
    message = anthropic_client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=history,
        tools=tools_spec,
        tool_choice={"type": "auto"}
    )
    history.append({"role": message.role, "content": message.content})

    # This loop handles chains of tool calls
    while message.stop_reason == "tool_use":
        tool_calls = [block for block in message.content if block.type == 'tool_use']

        tool_outputs = []
        for tool_call in tool_calls:
            tool_name = tool_call.name
            tool_input = tool_call.input
            tool_id = tool_call.id
            print(f"[AGENT] Calling Tool: `{tool_name}` with input `{tool_input}`")

            if tool_name in AVAILABLE_TOOLS:
                function_to_call = AVAILABLE_TOOLS[tool_name]
                try:
                    output = function_to_call(**tool_input)
                    tool_outputs.append({
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": json.dumps(output)
                    })
                except Exception as e:
                    print(f"[AGENT] ERROR calling tool: {e}")
                    tool_outputs.append({
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": json.dumps({"status": "error", "message": str(e)})
                    })

        # Append all tool results to the history
        history.append({"role": "user", "content": tool_outputs})

        # Make a second call to Claude with the tool results
        message = anthropic_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=history,
            tools=tools_spec,
            tool_choice={"type": "auto"}
        )
        history.append({"role": message.role, "content": message.content})

    return history

# --- Command-Line Test Block ---
if __name__ == "__main__":
    print("--- Starting Synapse Trader Demo ---")

    conversation_history = []

    # --- Turn 1: User asks for a quote ---
    user_message_1 = "Can I get a quote on 25 million dollar-sterling for 3 months for ClientCorp?"
    conversation_history.append({"role": "user", "content": user_message_1})
    conversation_history = run_conversation_turn(conversation_history)

    final_response = next(
        (block.text for block in conversation_history[-1]['content'] if hasattr(block, 'text')),
        "No text response found."
    )
    print(f"Synapse: {final_response}")

    # --- Turn 2: User books the trade ---
    user_message_2 = "Looks good. Done, book it."
    conversation_history.append({"role": "user", "content": user_message_2})
    conversation_history = run_conversation_turn(conversation_history)

    final_response = next(
        (block.text for block in conversation_history[-1]['content'] if hasattr(block, 'text')),
        "No text response found."
    )
    print(f"Synapse: {final_response}")

    print("\n--- Demo Finished ---")
