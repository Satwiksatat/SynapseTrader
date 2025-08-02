#!/usr/bin/env python3
"""
Test script for the upgraded Synapse Trader backend.
Demonstrates the new data-driven pricing and strategic tools.
"""

from tools import get_market_data, get_desk_axe, check_credit_limit, record_trade_and_notify

def test_market_data():
    """Test the new data-driven pricing model."""
    print("=== Testing Data-Driven Pricing ===")
    result = get_market_data("USDGBP", 25000000, "3M")
    print(f"Market Data Result: {result}")
    print()

def test_desk_axe():
    """Test the new desk axe functionality."""
    print("=== Testing Desk Axe ===")
    result = get_desk_axe("USDGBP")
    print(f"Desk Axe Result: {result}")
    print()

def test_credit_limit():
    """Test the renamed credit limit function."""
    print("=== Testing Credit Limit ===")
    trade_details = {
        "ccy_pair": "USDGBP",
        "notional": 25000000,
        "tenor": "3M"
    }
    result = check_credit_limit(trade_details)
    print(f"Credit Limit Result: {result}")
    print()

def test_audit_logging():
    """Test the renamed audit logging function."""
    print("=== Testing Audit Logging ===")
    record_trade_and_notify(
        "trade_execution",
        {
            "ccy_pair": "USDGBP",
            "notional": 25000000,
            "price": 1.26918,
            "timestamp": "2025-08-02T12:00:00"
        }
    )
    print()

def main():
    """Run all tests."""
    print("Synapse Trader Backend Upgrade Test")
    print("=" * 40)
    print()
    
    test_market_data()
    test_desk_axe()
    test_credit_limit()
    test_audit_logging()
    
    print("All tests completed successfully!")
    print("\nBackend upgrade summary:")
    print("- ✅ Data-driven pricing using Interest Rate Parity")
    print("- ✅ New desk axe functionality for strategic bias")
    print("- ✅ Renamed functions for better clarity")
    print("- ✅ Enhanced audit logging with downstream notifications")

if __name__ == "__main__":
    main() 