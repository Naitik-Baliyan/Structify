#!/usr/bin/env python
"""Test what's wrong with the browser"""

import requests
import json

print("=" * 60)
print("BROWSER DIAGNOSTIC - TESTING ALL SYSTEMS")
print("=" * 60)
print()

# Test 1: Frontend files
print("[TEST 1] Frontend Files Being Served")
print("-" * 60)
files = {
    'chat.html': 'Main HTML',
    'config.js': 'Configuration',
    'chat.js': 'Chat Logic',
    'auth.js': 'Authentication',
    'style.css': 'Styles'
}

for file, desc in files.items():
    try:
        r = requests.head(f'http://127.0.0.1:5500/{file}', timeout=3)
        status = "✅" if r.status_code == 200 else "❌"
        print(f"{status} {file:20} → {r.status_code} ({desc})")
    except Exception as e:
        print(f"❌ {file:20} → ERROR: {str(e)[:40]}")

print()

# Test 2: Chat HTML content
print("[TEST 2] Chat HTML Content")
print("-" * 60)
try:
    r = requests.get('http://127.0.0.1:5500/chat.html', timeout=3)
    content = r.text
    
    checks = {
        'DOCTYPE': '<!DOCTYPE' in content,
        'Chat Messages Div': 'id="chatMessages"' in content,
        'User Input Field': 'id="userInput"' in content,
        'Send Button': 'id="sendBtn"' in content,
        'BRD Modal': 'id="brdModal"' in content,
        'Script - config.js': 'config.js' in content,
        'Script - chat.js': 'chat.js' in content,
        'Script - auth.js': 'auth.js' in content,
    }
    
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
        
except Exception as e:
    print(f"❌ Error fetching HTML: {e}")

print()

# Test 3: Config file content
print("[TEST 3] Config.js Content")
print("-" * 60)
try:
    r = requests.get('http://127.0.0.1:5500/config.js', timeout=3)
    content = r.text
    
    checks = {
        'API_CONFIG defined': 'const API_CONFIG' in content,
        'BACKEND_URL set': 'BACKEND_URL' in content,
        'TIMEOUT configured': 'TIMEOUT' in content,
        'Port 8001': '8001' in content,
    }
    
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}")
    
    # Extract actual URL
    import re
    match = re.search(r"BACKEND_URL:\s*['\"]([^'\"]+)['\"]", content)
    if match:
        print(f"\n   Configured Backend URL: {match.group(1)}")
        
except Exception as e:
    print(f"❌ Error fetching config: {e}")

print()

# Test 4: Backend endpoints
print("[TEST 4] Backend Endpoints")
print("-" * 60)

# Health check
try:
    r = requests.get('http://127.0.0.1:8001/', timeout=3)
    print(f"✅ GET / → {r.status_code}")
except Exception as e:
    print(f"❌ GET / → {e}")

# Analyze endpoint
try:
    r = requests.post('http://127.0.0.1:8001/analyze', 
                     json={'idea': 'Test', 'target_market': 'Test', 'problem_statement': 'Test'},
                     timeout=5)
    print(f"✅ POST /analyze → {r.status_code}")
    data = r.json()
    print(f"   - Score: {data.get('compatibility_score', 'N/A')}")
    print(f"   - Has tags: {bool(data.get('domain_tags', []))}")
except Exception as e:
    print(f"❌ POST /analyze → {e}")

# BRD endpoint
try:
    test_data = {
        'idea': 'Test',
        'target_market': 'Market',
        'problem_statement': 'Problem',
        'analysis': 'Analysis',
        'compatibility_score': 75,
        'improvement_suggestions': ['Improve'],
        'risk_level': 'medium',
        'domain_tags': ['Tech']
    }
    r = requests.post('http://127.0.0.1:8001/generate_brd',
                     json={'analysis_data': test_data, 'format': 'txt'},
                     timeout=5)
    print(f"✅ POST /generate_brd → {r.status_code}")
except Exception as e:
    print(f"❌ POST /generate_brd → {e}")

print()

# Test 5: CORS Headers
print("[TEST 5] CORS Headers Check")
print("-" * 60)
try:
    r = requests.options('http://127.0.0.1:8001/analyze', 
                        headers={'Origin': 'http://127.0.0.1:5500'},
                        timeout=3)
    print(f"✅ OPTIONS request → {r.status_code}")
    
    cors_headers = {
        'Access-Control-Allow-Origin': r.headers.get('access-control-allow-origin', 'NOT SET'),
        'Access-Control-Allow-Methods': r.headers.get('access-control-allow-methods', 'NOT SET'),
        'Access-Control-Allow-Headers': r.headers.get('access-control-allow-headers', 'NOT SET'),
    }
    
    for header, value in cors_headers.items():
        if value != 'NOT SET':
            print(f"   ✅ {header}: {value[:50]}")
        else:
            print(f"   ❌ {header}: {value}")
            
except Exception as e:
    print(f"❌ CORS check → {e}")

print()
print("=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
