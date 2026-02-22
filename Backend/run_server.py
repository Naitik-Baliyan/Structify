#!/usr/bin/env python
"""Run the FastAPI server with uvicorn"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting Structify Backend Server...")
    print("📍 URL: http://127.0.0.1:8000")
    print("📍 API Docs: http://127.0.0.1:8000/docs")
    print("✅ CORS: Enabled for all origins (prototype demo)")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
        log_level="info"
    )
