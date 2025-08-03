"""
Trading tools and utilities for Synapse Trader.
Provides functions for market data access, risk assessment, and audit logging.
"""

import time
import pandas as pd
from datetime import datetime
import json
import os
from typing import Any
from elevenlabs.client import ElevenLabs

# Initialize ElevenLabs client
eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Load the WRDS data at module level
try:
    df_rates = pd.read_csv("./data/wrds_swap_data.csv")
except Exception as e:
    print(f"Error loading WRDS data: {str(e)}")
    df_rates = pd.DataFrame()

def get_client_info(client_id: str = None) -> dict:
    """
    Retrieve client portfolio and preferences.
    
    Args:
        client_id: Optional client identifier
        
    Returns:
        dict: Client information including portfolio and preferences
    """
    # In a real application, this would query a database.
    # For this example, we'll use a hardcoded dictionary.
    client_data = {
        'ClientCorp': {
            "risk_tolerance": "moderate",
            "investment_horizon": "medium-term",
            "portfolio_value": 1000000,
            "preferred_assets": ["equities", "fixed_income"]
        },
        'MegaFund': {
            "risk_tolerance": "high",
            "investment_horizon": "long-term",
            "portfolio_value": 50000000,
            "preferred_assets": ["equities", "derivatives"]
        },
        'GlobalInvest': {
            "risk_tolerance": "low",
            "investment_horizon": "short-term",
            "portfolio_value": 5000000,
            "preferred_assets": ["fixed_income", "cash"]
        }
    }
    return client_data.get(client_id, {
        "risk_tolerance": "unknown",
        "investment_horizon": "unknown",
        "portfolio_value": 0,
        "preferred_assets": []
    })

def get_market_data(ccy_pair: str = "USDGBP", notional_usd: int = 25000000, tenor: str = "3M") -> dict:
    """
    Get market data and calculate FX forward pricing using Interest Rate Parity.
    Data is fetched from the local wrds_swap_data.csv file.
    """
    try:
        if df_rates.empty:
            raise ValueError("WRDS data DataFrame is empty.")

        latest_date = df_rates['date'].max()
        df_latest = df_rates[df_rates['date'] == latest_date]
        
        usd_rate_3m = df_latest[df_latest['currency'] == 'USD']['rate'].iloc[0]
        gbp_rate_3m = df_latest[df_latest['currency'] == 'GBP']['rate'].iloc[0]
        spot_rate = 1.2725 

        days = 90
        all_in_price = spot_rate * (((1 + gbp_rate_3m * (days/365))) / (1 + usd_rate_3m * (days/360)))
        all_in_price = round(all_in_price, 5)

        forward_points = round((all_in_price - spot_rate) * 10000, 1)

        return { 
            "status": "success", 
            "all_in_price": all_in_price, 
            "forward_points": forward_points,
            "spot_rate": spot_rate,
            "usd_rate_3m": usd_rate_3m,
            "gbp_rate_3m": gbp_rate_3m
        }
        
    except Exception as e:
        print(f"Error in market data calculation: {str(e)}")
        return {"status": "error", "message": str(e)}

def get_desk_axe(ccy_pair: str) -> dict:
    """Returns the trading desk's current strategy (axe) for a currency pair."""
    strategy = { "USDGBP": {"direction": "BUY", "currency": "GBP", "intensity": "HIGH"} }
    if ccy_pair in strategy:
        return {"status": "success", "axe": strategy[ccy_pair]}
    else:
        return {"status": "success", "axe": {"direction": "NEUTRAL"}}

def check_credit_limit(client_id: str, notional_usd: float) -> dict:
    """
    Checks if a trade for a given client is within their trading limits.
    """
    limits = {
        'ClientCorp': 50_000_000.0,
        'MegaFund': 200_000_000.0,
        'GlobalInvest': 100_000_000.0
    }
    client_limit = limits.get(client_id)

    if client_limit is None:
        return {"status": "failure", "message": f"Client '{client_id}' not found."}

    if notional_usd > client_limit:
        return {
            "status": "failure", 
            "message": f"Notional of {notional_usd:,.2f} exceeds limit of {client_limit:,.2f} for {client_id}."
        }

    return {"status": "success", "message": f"Trade within limits for {client_id}."}

def record_trade_and_notify(client_id: str, notional_usd: float, price: float, ccy_pair: str, tenor: str, side: str) -> dict:
    """
    Records the details of a completed trade locally and generates a voice notification.
    """
    try:
        transaction_id = f"TXN-{int(time.time())}"
        
        trade_data = {
            "tx_id": transaction_id,
            "client_id": client_id,
            "ccy_pair": ccy_pair,
            "notional_usd": notional_usd,
            "tenor": tenor,
            "price": price,
            "side": side,
            "booked_at": datetime.utcnow().isoformat()
        }
        
        # In a real application, this would write to a database or a file.
        # For this example, we'll just log it to the console.
        print(f"[TRADE RECORDED]: {json.dumps(trade_data)}")

        notification_text = f"Trade booked successfully. Transaction ID {transaction_id}."
        audio = eleven_client.text_to_speech.convert(
            text=notification_text,
            voice_id="Josh",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )
        
        os.makedirs("audio_outputs", exist_ok=True)
        with open(f"audio_outputs/{transaction_id}.mp3", "wb") as f:
            f.write(audio)
        
        return {"status": "success", "transaction_id": transaction_id}
            
    except Exception as e:
        print(f"Error recording trade: {e}")
        return {"status": "error", "message": str(e)}

def check_trading_risk(notional_usd: float) -> dict:
    """
    Checks if a trade is within the desk's internal trading risk limits.
    """
    max_notional = 75_000_000.0

    if notional_usd > max_notional:
        return {
            "status": "failure",
            "message": f"Trade size of {notional_usd:,.2f} exceeds the desk's max trade limit of {max_notional:,.2f}."
        }
    
    return {"status": "success", "message": "Trade is within desk risk limits."}
