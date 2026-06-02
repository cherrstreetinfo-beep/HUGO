#!/usr/bin/env python3
"""
HUGO - Self-Hosted AI Operating System
Main entry point for the FastAPI application
"""

import uvicorn
from app.main import create_app
import os
from pathlib import Path

if __name__ == "__main__":
    app = create_app()
    
    port = int(os.getenv("API_PORT", 8001))
    host = os.getenv("API_HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        debug=debug,
        log_level="info"
    )
