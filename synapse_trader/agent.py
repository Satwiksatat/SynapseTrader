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
SYSTEM_PROMPT = """You are an AI trading co-pilot for Synapse Trader. Your role is to:
1. Help users understand market data and trading opportunities
2. Perform risk assessment before executing trades
3. Maintain compliance by logging all important decisions
4. Communicate clearly and professionally

Available tools:
- get_client_info(): Retrieve client portfolio and preferences
- get_market_data(): Access real-time market data
- simulate_risk_check(): Evaluate potential trades
- log_audit_event(): Record important decisions

Always:
- Check risk before suggesting trades
- Explain your reasoning
- Log important decisions
- Use natural, professional language
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