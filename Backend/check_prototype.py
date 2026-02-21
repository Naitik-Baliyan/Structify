#!/usr/bin/env python3
"""
Complete Structify Prototype Health Check
==========================================
Comprehensive verification of both backend and frontend integration
"""

import os
import json
import sys
from pathlib import Path

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def check_backend_files():
    """Verify all backend files exist"""
    print_header("1️⃣  BACKEND FILE CHECK")
    
    backend_path = Path(r"c:\Users\ASUS\Desktop\Structify\Backend")
    required_files = {
        "main.py": "FastAPI application",
        "requirements.txt": "Python dependencies",
        ".env": "Environment configuration",
        "test_api.py": "Testing suite",
        "services/ai_engine.py": "AI Engine service",
        "services/__init__.py": "Service package",
    }
    
    all_good = True
    for file, description in required_files.items():
        filepath = backend_path / file
        exists = filepath.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {file:<30} - {description}")
        if not exists:
            all_good = False
    
    return all_good

def check_frontend_files():
    """Verify all frontend files exist"""
    print_header("2️⃣  FRONTEND FILE CHECK")
    
    frontend_path = Path(r"c:\Users\ASUS\Desktop\Structify\Frontend")
    required_files = {
        "index.html": "Home page",
        "login.html": "Login page",
        "chat.html": "Chat interface",
        "chat.js": "Chat logic",
        "config.js": "API configuration",
        "auth.js": "Authentication",
        "script.js": "Main script",
        "style.css": "Styling",
    }
    
    all_good = True
    for file, description in required_files.items():
        filepath = frontend_path / file
        exists = filepath.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {file:<20} - {description}")
        if not exists:
            all_good = False
    
    return all_good

def check_backend_imports():
    """Verify backend imports work"""
    print_header("3️⃣  BACKEND MODULE CHECK")
    
    try:
        sys.path.insert(0, r"c:\Users\ASUS\Desktop\Structify\Backend")
        
        # Test imports
        try:
            import main
            print("  ✅ main.py imports successfully")
        except Exception as e:
            print(f"  ❌ main.py import failed: {str(e)}")
            return False
        
        try:
            from services import generate_analysis_response
            print("  ✅ services module imports successfully")
        except Exception as e:
            print(f"  ❌ services import failed: {str(e)}")
            return False
        
        try:
            from dotenv import load_dotenv
            print("  ✅ python-dotenv installed")
        except Exception as e:
            print(f"  ❌ python-dotenv not installed")
            return False
        
        try:
            import google.generativeai
            print("  ✅ google-generativeai installed")
        except Exception as e:
            print(f"  ❌ google-generativeai not installed")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Module check failed: {str(e)}")
        return False

def check_env_configuration():
    """Verify .env configuration"""
    print_header("4️⃣  ENVIRONMENT CONFIGURATION CHECK")
    
    env_path = Path(r"c:\Users\ASUS\Desktop\Structify\Backend\.env")
    
    if not env_path.exists():
        print("  ❌ .env file not found")
        return False
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        checks = {
            "API_PROVIDER": "API provider configured",
            "GEMINI_API_KEY": "Gemini API key set",
            "FRONTEND_ORIGIN": "CORS origin configured",
            "API_TIMEOUT": "API timeout configured"
        }
        
        all_good = True
        for key, description in checks.items():
            if key in content:
                # Check if it has actual value
                if f"{key}=" in content:
                    value_line = [line for line in content.split('\n') if line.startswith(key)][0]
                    has_value = not value_line.endswith("=")
                    if has_value:
                        print(f"  ✅ {description}")
                    else:
                        print(f"  ⚠️  {description} (empty value)")
                        all_good = False
            else:
                print(f"  ❌ {description} (not found)")
                all_good = False
        
        return all_good
    except Exception as e:
        print(f"  ❌ Error reading .env: {str(e)}")
        return False

def check_api_endpoints():
    """Test backend API endpoints"""
    print_header("5️⃣  HOST URL CHECK")
    
    try:
        import requests
        
        print("  Testing backend availability...")
        base_url = "http://127.0.0.1:8000"
        
        try:
            response = requests.get(f"{base_url}/", timeout=5)
            if response.status_code == 200:
                print(f"  ✅ Backend is running at {base_url}")
                print(f"     Response: {response.json()['message']}")
            else:
                print(f"  ⚠️  Backend responded with status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            print(f"  ⚠️  Backend not running (expected if not started)")
            print(f"     Start it with: python -m uvicorn main:app --reload")
            return None  # Not an error, just not running yet
        
        return True
    except Exception as e:
        print(f"  ⚠️  Could not test API: {str(e)}")
        return None

def check_frontend_config():
    """Verify frontend is configured for backend"""
    print_header("6️⃣  FRONTEND BACKEND INTEGRATION CHECK")
    
    config_path = Path(r"c:\Users\ASUS\Desktop\Structify\Frontend\config.js")
    
    if not config_path.exists():
        print("  ❌ config.js not found")
        return False
    
    try:
        with open(config_path, 'r') as f:
            content = f.read()
        
        checks = {
            "API_CONFIG": "API configuration object exists",
            "BACKEND_URL": "Backend URL configured",
            "127.0.0.1:8000": "Correct backend host"
        }
        
        all_good = True
        for key, description in checks.items():
            if key in content:
                print(f"  ✅ {description}")
            else:
                print(f"  ❌ {description}")
                all_good = False
        
        return all_good
    except Exception as e:
        print(f"  ❌ Error reading config.js: {str(e)}")
        return False

def check_documentation():
    """Verify documentation files"""
    print_header("7️⃣  DOCUMENTATION CHECK")
    
    backend_path = Path(r"c:\Users\ASUS\Desktop\Structify\Backend")
    doc_files = [
        "README.md",
        "QUICK_START.md",
        "BACKEND_SETUP.md",
        "START_HERE.md"
    ]
    
    all_good = True
    for doc in doc_files:
        filepath = backend_path / doc
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"  ✅ {doc:<30} ({size:,} bytes)")
        else:
            print(f"  ❌ {doc:<30} (missing)")
            all_good = False
    
    return all_good

def print_summary(results):
    """Print final summary"""
    print_header("📊 COMPLETE PROTOTYPE STATUS")
    
    checks = [
        ("Backend Files", results[0]),
        ("Frontend Files", results[1]),
        ("Backend Modules", results[2]),
        ("Environment Config", results[3]),
        ("API Endpoints", results[4]),
        ("Frontend Integration", results[5]),
        ("Documentation", results[6])
    ]
    
    passed = sum(1 for _, r in checks if r is True)
    failed = sum(1 for _, r in checks if r is False)
    pending = sum(1 for _, r in checks if r is None)
    
    print("Results:")
    for name, result in checks:
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⚠️  PENDING"
        print(f"  {status} - {name}")
    
    print()
    print(f"Summary: {passed} passed, {failed} failed, {pending} pending \n")
    
    if failed == 0 and pending == 0:
        print("🎉 PROTOTYPE IS FULLY RUNNING! 🎉\n")
        print("Your Structify application is ready:")
        print("  ✅ Backend: http://127.0.0.1:8000")
        print("  ✅ Frontend: Open Frontend/index.html or Frontend/login.html")
        print("  ✅ Chat: Open Frontend/chat.html (after login)")
        print("  ✅ API: POST /analyze with business ideas")
        return True
    elif failed == 0 and passed > 4:
        print("⚡ PROTOTYPE IS MOSTLY RUNNING!\n")
        print("Action Items:")
        if pending > 0:
            print("  • Start backend server: python -m uvicorn main:app --reload")
        return True
    else:
        print("❌ ISSUES FOUND - Please fix the failed checks above")
        return False

def main():
    print("\n╔════════════════════════════════════════════════════════════════════╗")
    print("║                                                                    ║")
    print("║          STRUCTIFY COMPLETE PROTOTYPE HEALTH CHECK                ║")
    print("║                  February 21, 2026                                ║")
    print("║                                                                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    
    # Run all checks
    results = [
        check_backend_files(),
        check_frontend_files(),
        check_backend_imports(),
        check_env_configuration(),
        check_api_endpoints(),
        check_frontend_config(),
        check_documentation()
    ]
    
    # Print summary
    success = print_summary(results)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
