"""
Trading tools and utilities for Synapse Trader.
Provides functions for market data access, risk assessment, and audit logging.
"""

import time
import pandas as pd
from datetime import datetime
import json
import os
from typing import Dict, Any

# Load the WRDS data at module level
try:
    df_rates = pd.read_csv("data/wrds_swap_data.csv")
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
    # Simulated client data
    return {
        "risk_tolerance": "moderate",
        "investment_horizon": "medium-term",
        "portfolio_value": 1000000,
        "preferred_assets": ["equities", "fixed_income"]
    }

def get_market_data(ccy_pair: str = "USDGBP", notional_usd: int = 25000000, tenor: str = "3M") -> dict:
    """
    Get market data and calculate FX forward pricing using Interest Rate Parity.
    """
    print(f"[TOOLS] Getting market data for {ccy_pair} {tenor}...")
    
    try:
        if df_rates.empty:
            raise ValueError("WRDS data DataFrame is empty.")

        latest_date = df_rates['date'].max()
        df_latest = df_rates[df_rates['date'] == latest_date]
        
        # --- THIS IS THE CORRECTED LOGIC ---
        usd_rate_3m = df_latest[df_latest['currency'] == 'USD']['rate'].iloc[0]
        gbp_rate_3m = df_latest[df_latest['currency'] == 'GBP']['rate'].iloc[0]
        # ------------------------------------

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
    print(f"[TOOLS] Getting desk axe for {ccy_pair}...")
    strategy = { "USDGBP": {"direction": "BUY", "currency": "GBP", "intensity": "HIGH"} }
    if ccy_pair in strategy:
        return {"status": "success", "axe": strategy[ccy_pair]}
    else:
        return {"status": "success", "axe": {"direction": "NEUTRAL"}}

def check_credit_limit(client_id: str, notional_usd: float) -> Dict[str, Any]:
    """
    Checks if a trade for a given client is within their trading limits.
    """
    print(f"[TOOLS] Checking credit limit for {client_id}...")
    
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

def record_trade_and_notify(client_id: str, notional_usd: float, price: float) -> Dict[str, Any]:
    """
    Records the details of a completed trade for audit and notifies settlements.
    """
    print(f"[TOOLS] Auditing trade for {client_id} of {notional_usd:,.2f} USD at {price}...")
    
    # Generate a unique-looking transaction ID for the demo
    transaction_id = f"TXN-{int(time.time())}"
    
    print(f"[AUDIT] Trade booked. Transaction ID: {transaction_id}")
    print("[AUDIT] Notifying Middle Office / Settlements...")
    
    return {"status": "success", "transaction_id": transaction_id}
    
    # Ensure the log entry is JSON serializable
    try:
        json.dumps(log_entry)
    except:
        log_entry["details"] = str(details)
    
    # Print to console for now
    # In production, this would write to a secure audit log
    print(f"AUDIT LOG: {json.dumps(log_entry)}")

def check_trading_risk(notional_usd: float) -> Dict[str, Any]:
    """
    Checks if a trade is within the desk's internal trading risk limits.
    """
    print(f"[TOOLS] Checking trading risk for notional {notional_usd:,.2f} USD...")
    
    # Hardcoded desk limits for the demo
    MAX_NOTIONAL_PER_TRADE = 75_000_000.0

    if notional_usd > MAX_NOTIONAL_PER_TRADE:
        return {
            "status": "failure",
            "message": f"Trade size of {notional_usd:,.2f} exceeds the desk's max trade limit of {MAX_NOTIONAL_PER_TRADE:,.2f}."
        }
    
    return {"status": "success", "message": "Trade is within desk risk limits."}
    # Time Complexity: O(1)