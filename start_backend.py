#!/usr/bin/env python3
"""
Startup script for Synapse Trader FastAPI backend.
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_dependencies():
    """Check if required environment variables are set."""
    required_vars = ["ELEVENLABS_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your .env file")
        return False
    
    print("✅ Environment variables loaded successfully")
    return True

def main():
    """Start the FastAPI server."""
    print("🚀 Starting Synapse Trader Backend...")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ main.py not found. Please ensure you're in the correct directory.")
        sys.exit(1)
    
    print("📡 Starting FastAPI server on http://localhost:8000")
    print("📚 API documentation available at http://localhost:8000/docs")
    print("🔍 Health check available at http://localhost:8000/api/health")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 