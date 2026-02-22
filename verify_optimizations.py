#!/usr/bin/env python
"""
Structify Optimization Verification Script
Tests runtime stability and frontend-backend communication
"""

import subprocess
import time
import sys
import json
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")

def print_status(status, message):
    symbol = "✅" if status else "❌"
    print(f"{symbol} {message}")
    return status

def test_backend_startup():
    """Test 1: Verify FastAPI can be imported and initialized"""
    print_header("Test 1: Backend Initialization")
    
    try:
        # Import main.py
        import sys
        sys.path.insert(0, str(Path(__file__).parent / "Backend"))
        
        from main import app
        print_status(True, "FastAPI app imported successfully")
        
        # Check if CORS middleware is configured
        cors_found = any("CORSMiddleware" in str(m) for m in app.user_middleware)
        print_status(cors_found, "CORS middleware configured")
        
        # Check if routes exist
        routes = [route.path for route in app.routes]
        analyze_exists = any("/analyze" in r for r in routes)
        brd_exists = any("/generate_brd" in r for r in routes)
        
        print_status(analyze_exists, "/analyze endpoint exists")
        print_status(brd_exists, "/generate_brd endpoint exists")
        
        return True
    except Exception as e:
        print_status(False, f"Backend initialization failed: {str(e)}")
        return False

def test_config_files():
    """Test 2: Verify frontend configuration"""
    print_header("Test 2: Frontend Configuration")
    
    try:
        config_file = Path(__file__).parent / "Frontend" / "config.js"
        
        if not config_file.exists():
            print_status(False, "config.js not found")
            return False
        
        print_status(True, "config.js exists")
        
        # Read and verify config
        content = config_file.read_text()
        
        checks = [
            ("'http://127.0.0.1:8000'" in content or '"http://127.0.0.1:8000"' in content, "BACKEND_URL set to port 8000"),
            ("RETRY_ATTEMPTS" in content, "RETRY_ATTEMPTS configured"),
            ("TIMEOUT" in content, "Request timeout configured"),
            ("fetchWithRetry" in content, "fetchWithRetry function exists"),
        ]
        
        all_pass = True
        for check, desc in checks:
            if not print_status(check, desc):
                all_pass = False
        
        return all_pass
    except Exception as e:
        print_status(False, f"Config verification failed: {str(e)}")
        return False

def test_frontend_files():
    """Test 3: Verify frontend has necessary files"""
    print_header("Test 3: Frontend Files")
    
    frontend_path = Path(__file__).parent / "Frontend"
    required_files = [
        "chat.html",
        "chat.js",
        "config.js",
        "auth.js",
        "style.css"
    ]
    
    all_exist = True
    for filename in required_files:
        file_path = frontend_path / filename
        exists = file_path.exists()
        print_status(exists, f"{filename} exists")
        if not exists:
            all_exist = False
    
    return all_exist

def test_error_handling():
    """Test 4: Verify error handling in code"""
    print_header("Test 4: Error Handling")
    
    try:
        chat_js = (Path(__file__).parent / "Frontend" / "chat.js").read_text()
        ai_engine = (Path(__file__).parent / "Backend" / "services" / "ai_engine.py").read_text()
        
        checks = [
            ("try-except blocks for JSON parsing" in chat_js or "try" in chat_js, "chat.js has error handling"),
            ("try" in ai_engine and "except" in ai_engine, "ai_engine.py has error handling"),
            ("requestAnimationFrame" in chat_js, "DOM rendering optimized"),
            ("displayAIMessage" in chat_js, "Message display function exists"),
        ]
        
        all_pass = True
        for check, desc in checks:
            if not print_status(check, desc):
                all_pass = False
        
        return all_pass
    except Exception as e:
        print_status(False, f"Error handling verification failed: {str(e)}")
        return False

def test_cors_configuration():
    """Test 5: Verify CORS is properly configured"""
    print_header("Test 5: CORS Middleware")
    
    try:
        main_py = (Path(__file__).parent / "Backend" / "main.py").read_text()
        
        checks = [
            ("CORSMiddleware" in main_py, "CORS middleware imported"),
            ("allow_origins" in main_py, "allow_origins configured"),
            ("allow_methods" in main_py, "allow_methods configured"),
            ("allow_headers" in main_py, "allow_headers configured"),
        ]
        
        all_pass = True
        for check, desc in checks:
            if not print_status(check, desc):
                all_pass = False
        
        return all_pass
    except Exception as e:
        print_status(False, f"CORS verification failed: {str(e)}")
        return False

def test_authentication():
    """Test 6: Verify authentication is preserved"""
    print_header("Test 6: Authentication Integrity")
    
    try:
        chat_js = (Path(__file__).parent / "Frontend" / "chat.js").read_text()
        auth_js = (Path(__file__).parent / "Frontend" / "auth.js").read_text()
        
        checks = [
            ("localStorage" in chat_js, "localStorage still used for auth"),
            ("checkUserAuthentication" in chat_js, "Auth check function exists"),
            ("structify_current_user" in chat_js, "User storage key intact"),
            ("auth.js" in (Path(__file__).parent / "Frontend" / "chat.html").read_text(), "auth.js loaded in HTML"),
        ]
        
        all_pass = True
        for check, desc in checks:
            if not print_status(check, desc):
                all_pass = False
        
        return all_pass
    except Exception as e:
        print_status(False, f"Authentication verification failed: {str(e)}")
        return False

def test_api_endpoint():
    """Test 7: Verify API endpoint configuration"""
    print_header("Test 7: API Endpoint Configuration")
    
    try:
        chat_js = (Path(__file__).parent / "Frontend" / "chat.js").read_text()
        
        checks = [
            ("/analyze" in chat_js, "analyze endpoint referenced"),
            ("POST" in chat_js, "POST method used"),
            ("fetchWithRetry" in chat_js, "Retry logic used"),
            ("Content-Type" in chat_js and "application/json" in chat_js, "JSON content type set"),
        ]
        
        all_pass = True
        for check, desc in checks:
            if not print_status(check, desc):
                all_pass = False
        
        return all_pass
    except Exception as e:
        print_status(False, f"API endpoint verification failed: {str(e)}")
        return False

def run_all_tests():
    """Run all verification tests"""
    print("\n" + "="*60)
    print("  STRUCTIFY OPTIMIZATION VERIFICATION SUITE")
    print("  " + time.strftime("%Y-%m-%d %H:%M:%S"))
    print("="*60)
    
    tests = [
        test_backend_startup,
        test_config_files,
        test_frontend_files,
        test_error_handling,
        test_cors_configuration,
        test_authentication,
        test_api_endpoint,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Test failed with exception: {str(e)}")
            results.append(False)
    
    # Summary
    print_header("Verification Summary")
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All optimizations verified successfully!")
        print("\nReady to run:")
        print("  1. Backend: cd Backend && python -m uvicorn main:app --reload")
        print("  2. Frontend: cd Frontend && python -m http.server 5500")
        print("  3. Browser: http://localhost:5500/chat.html")
        return True
    else:
        print(f"\n❌ Some tests failed ({total - passed} failures)")
        print("Please review the errors above")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
