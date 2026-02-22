#!/usr/bin/env python
"""Start backend server using uvicorn correctly"""

import subprocess
import sys
import time

print("🚀 Starting Structify Backend Server...")
print("📍 URL: http://127.0.0.1:8000")
print("📍 API Docs: http://127.0.0.1:8000/docs")
print("✅ CORS: Enabled for all origins (prototype demo)")
print("\nPress Ctrl+C to stop the server\n")

# Run uvicorn with proper import string
subprocess.run([
    sys.executable, "-m", "uvicorn", 
    "main:app",
    "--host", "127.0.0.1",
    "--port", "8000",
    "--reload"
], cwd="C:\\Users\\ASUS\\Desktop\\Structify\\Backend")
