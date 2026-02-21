#!/usr/bin/env python3
"""
CORS and Backend Connectivity Test
"""

import requests
import json

print('\n' + '='*60)
print('CORS & BACKEND CONNECTIVITY TEST')
print('='*60 + '\n')

# Test 1: Backend Health
print('[1] Backend Health Check')
print('-'*60)
try:
    response = requests.get('http://127.0.0.1:8001/', timeout=2)
    if response.status_code == 200:
        print('✅ Backend is ALIVE at http://127.0.0.1:8001')
        print(f'   Response: {response.json()}')
    else:
        print(f'❌ Backend status: {response.status_code}')
except Exception as e:
    print(f'❌ Backend not accessible: {e}')

print()

# Test 2: Simple POST without Origin
print('[2] POST to /analyze (no Origin header)')
print('-'*60)
try:
    response = requests.post(
        'http://127.0.0.1:8001/analyze',
        json={
            'idea': 'Test idea',
            'target_market': 'Test market',
            'problem_statement': 'Test problem'
        },
        headers={'Content-Type': 'application/json'},
        timeout=5
    )
    if response.status_code == 200:
        print(f'✅ /analyze works! Status: {response.status_code}')
        data = response.json()
        print(f'   Score: {data.get("compatibility_score")}/100')
    else:
        print(f'❌ /analyze failed: {response.status_code}')
except Exception as e:
    print(f'❌ Error: {e}')

print()

# Test 3: POST with localhost:5500 Origin
print('[3] POST to /analyze (from localhost:5500)')
print('-'*60)
try:
    response = requests.post(
        'http://127.0.0.1:8001/analyze',
        json={
            'idea': 'Test idea',
            'target_market': 'Test market',
            'problem_statement': 'Test problem'
        },
        headers={
            'Content-Type': 'application/json',
            'Origin': 'http://localhost:5500'
        },
        timeout=5
    )
    print(f'Status: {response.status_code}')
    cors_header = response.headers.get('access-control-allow-origin', 'NOT SET')
    print(f'CORS Header: {cors_header}')
    
    if response.status_code == 200:
        data = response.json()
        print(f'✅ Request successful!')
        print(f'   Score: {data.get("compatibility_score")}/100')
    else:
        print(f'❌ Request failed: {response.status_code}')
        
except Exception as e:
    print(f'❌ Error: {e}')

print()

# Test 4: Frontend is serving
print('[4] Frontend Server Check')
print('-'*60)
try:
    response = requests.get('http://localhost:5500/chat.html', timeout=2)
    if response.status_code == 200:
        print(f'✅ Frontend is ALIVE at http://localhost:5500')
        print(f'   chat.html size: {len(response.content)} bytes')
    else:
        print(f'❌ Frontend status: {response.status_code}')
except Exception as e:
    print(f'❌ Frontend not accessible: {e}')

print()
print('='*60)
print('NEXT STEPS:')
print('  1. Open browser to: http://localhost:5500/chat.html')
print('  2. Open browser console: F12 → Console tab')
print('  3. Try the chat - watch for error messages')
print('  4. Check if "[chat.js] Backend URL:" message appears')
print('='*60 + '\n')
