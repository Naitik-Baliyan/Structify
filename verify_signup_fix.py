import requests

# Test signup fixes
print("=" * 60)
print("SIGNUP FIX VERIFICATION")
print("=" * 60)
print()

try:
    r = requests.get('http://127.0.0.1:5500/auth.js')
    print(f"✅ Auth.js loads: {r.status_code}")
    
    auth_code = r.text
    
    checks = {
        'authInitialized flag': 'let authInitialized = false' in auth_code,
        'formListenersSetup flag': 'let formListenersSetup = false' in auth_code,
        'directButtonListenersSetup flag': 'let directButtonListenersSetup = false' in auth_code,
        'isHandlingSignup flag': 'let isHandlingSignup = false' in auth_code,
        'isSignupInProgress flag': 'let isSignupInProgress = false' in auth_code,
        'handleSignup guard': 'if (isHandlingSignup)' in auth_code,
        'performSignup guard': 'if (isSignupInProgress)' in auth_code,
    }
    
    print("\nGuard Flag Verification:")
    print("-" * 60)
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
    
    all_pass = all(checks.values())
    print()
    print("=" * 60)
    if all_pass:
        print("✅ ALL SIGNUP FIXES VERIFIED")
        print("Signup button should now work consistently!")
    else:
        print("❌ Some checks failed - review fixes")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
