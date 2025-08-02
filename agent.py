"""
AI agent implementation for Synapse Trader.
Handles communication with Claude and manages trading tools.
"""

import os
import anthropic
from tools import get_client_info, get_market_data, simulate_risk_check, log_audit_event

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Master prompt for Claude
# in agent.py
SYSTEM_PROMPT = """You are SynapseTrader, a voice-enabled co-pilot...
...
• Mission: help a trader quote, negotiate, and book a plain-vanilla USD/GBP 3-month FX forward.
...
1. price_fx_forward
   Purpose: Return the all-in price and forward points for an FX forward.
   Signature: {"name": "price_fx_forward", "args": {"ccy_pair": "USDGBP", "notional_usd": 25000000, "tenor": "3M"}}
...etc.
"""

def process_user_input(user_message: str) -> str:
    """
    Process user input through Claude and return the response.
    
    Args:
        user_message: The user's query or command
        
    Returns:
        str: Claude's processed response
    """
    try:
        # Create message to Claude
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        
        # Process the response
        response = message.content[0].text
        
        # Log the interaction
        log_audit_event(
            event_type="user_interaction",
            details={
                "user_message": user_message,
                "ai_response": response
            }
        )
        
        return response
        
    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        log_audit_event(
            event_type="error",
            details={"error": error_msg}
        )
        return error_msg