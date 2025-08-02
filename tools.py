"""
Trading tools and utilities for Synapse Trader.
Provides functions for market data access, risk assessment, and audit logging.
"""

import time
import pandas as pd
from datetime import datetime
import time
import json
import os
from firebolt_client import execute

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

# ---------------------------------------------------------------------------
# FX Forward specific helper functions and simulated tool implementations
# ---------------------------------------------------------------------------

# Try to lazily load the latest FX market snapshot.  We purposely do this at
# import-time so that repeated calls to ``price_fx_forward`` are fast and use
# a consistent view of the market during the demo.
try:
    _fx_market_df: pd.DataFrame | None = pd.read_csv("data/wrds_fx_data.csv")
    # keep only the last (most recent) row for each currency pair
    _fx_market_df = (
        _fx_market_df.sort_values("Date").groupby("Pair", as_index=False).tail(1)
    )
except FileNotFoundError:
    # Fallback: create a single-row DataFrame with hard-coded example rates so
    # the demo always works even if the CSV is missing.
    _fx_market_df = pd.DataFrame(
        [
            {
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Pair": "USDGBP",
                "SpotRate": 1.2700,
                "3M_USD_Rate": 0.052,  # 5.2% p.a.
                "3M_GBP_Rate": 0.047,  # 4.7% p.a.
            }
        ]
    )


def _get_latest_fx_row(pair: str) -> dict:
    """Return the latest FX price row for the requested pair."""
    row_match = _fx_market_df[_fx_market_df["Pair"] == pair]
    if row_match.empty:
        raise ValueError(f"Unsupported currency pair: {pair}")
    return row_match.iloc[0].to_dict()


def price_fx_forward(ccy_pair: str, notional_usd: float, tenor: str):
    """Simulate pricing a USD/GBP FX Forward using Interest Rate Parity.

    Args:
        ccy_pair: Currently only supports "USDGBP" (base/quote order is USD/GBP)
        notional_usd: Trade size in USD terms.
        tenor: Forward tenor, e.g. "3M".

    Returns:
        JSON string containing the all-in forward rate, forward points and
        contextual description.
    """
    if tenor.upper() != "3M":
        raise ValueError("Only 3M tenors are supported in the MVP.")

    mkt = _get_latest_fx_row(ccy_pair)
    spot_rate = float(mkt["SpotRate"])
    usd_rate = float(mkt["3M_USD_Rate"])
    gbp_rate = float(mkt["3M_GBP_Rate"])

    # day-count simple approximation: 90/360 = 0.25 years
    forward_rate = spot_rate * ((1 + gbp_rate * 0.25) / (1 + usd_rate * 0.25))
    forward_points = (forward_rate - spot_rate) * 10_000  # points in pips

    # Persist market snapshot to Firebolt for analytics
    try:
        execute(
            "INSERT INTO market_snaps (ts, pair, spot, usd_3m, gbp_3m) VALUES (?, ?, ?, ?, ?)",
            [datetime.utcnow().isoformat(), ccy_pair, spot_rate, usd_rate, gbp_rate],
        )
    except Exception as exc:
        print(f"Firebolt insert failed (market_snaps): {exc}")

    return json.dumps(
        {
            "status": "success",
            "all_in_price": round(forward_rate, 5),
            "points": round(forward_points, 2),
            "details": f"Quote for {notional_usd/1_000_000:.1f}mm {ccy_pair} {tenor} forward.",
        }
    )


def check_limits(client_id: str, notional_usd: float, tenor: str):
    """Very simple limit check – fail trades over 50 mm notional."""
    if notional_usd > 50_000_000:
        return json.dumps(
            {
                "status": "failed",
                "reason": "Notional exceeds client credit limit.",
            }
        )
    return json.dumps({"status": "ok", "kyc_isda_status": "Active"})


def record_audit(trade_json: dict):
    """Persist the trade locally *and* in Firebolt, return transaction id."""
    tx_id = f"TXN-{int(time.time())}"
    ts_iso = datetime.utcnow().isoformat()

    # ------------------------------------------------------------------
    # Local JSON (fallback / offline demo)
    # ------------------------------------------------------------------
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", f"{tx_id}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(trade_json, f, indent=2)

    # ------------------------------------------------------------------
    # Firebolt persistence (trades & audit tables)
    # ------------------------------------------------------------------
    try:
        execute(
            "INSERT INTO trades (tx_id, client_id, ccy_pair, notional_usd, tenor, fwd_points, price, side, booked_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                tx_id,
                trade_json.get("client_id", "unknown"),
                trade_json.get("ccy_pair", "USDGBP"),
                trade_json.get("notional_usd", 0.0),
                trade_json.get("tenor", "3M"),
                trade_json.get("points", 0.0),
                trade_json.get("all_in_price", 0.0),
                trade_json.get("side", "buy"),
                ts_iso,
            ],
        )
        execute(
            "INSERT INTO audit (ts, event_type, payload) VALUES (?, ?, ?)",
            [ts_iso, "trade_booked", json.dumps(trade_json)],
        )
    except Exception as exc:
        print(f"Firebolt insert failed (trades/audit): {exc}")

    return json.dumps({"status": "booked", "transaction_id": tx_id})
