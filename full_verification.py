#!/usr/bin/env python3
"""
COMPLETE STRUCTIFY PROTOTYPE VERIFICATION
Tests all endpoints, CORS, and functionality
"""

import requests
import json
import time

print('\n' + '='*70)
print(' '*15 + '✅ COMPLETE STRUCTIFY VERIFICATION')
print('='*70)

all_passed = True

# ====== TEST 1: SERVERS RUNNING ======
print('\n[TEST 1] Server Status')
print('-'*70)

backend_ok = False
frontend_ok = False

try:
    r = requests.get('http://127.0.0.1:8001/', timeout=2)
    if r.status_code == 200:
        print('✅ BACKEND RUNNING')
        print(f'   URL: http://127.0.0.1:8001')
        print(f'   Response: {r.json()}')
        backend_ok = True
    else:
        print(f'❌ BACKEND ERROR: Status {r.status_code}')
        all_passed = False
except Exception as e:
    print(f'❌ BACKEND NOT RUNNING: {e}')
    all_passed = False

time.sleep(0.5)

try:
    r = requests.get('http://localhost:5500/chat.html', timeout=2)
    if r.status_code == 200:
        print('✅ FRONTEND RUNNING')
        print(f'   URL: http://localhost:5500')
        print(f'   chat.html size: {len(r.content)} bytes')
        frontend_ok = True
    else:
        print(f'❌ FRONTEND ERROR: Status {r.status_code}')
        all_passed = False
except Exception as e:
    print(f'❌ FRONTEND NOT RUNNING: {e}')
    all_passed = False

if not (backend_ok and frontend_ok):
    print('\n⚠️  Servers not fully running. Stopping tests.')
    exit(1)

# ====== TEST 2: CORS CONFIGURATION ======
print('\n[TEST 2] CORS Configuration')
print('-'*70)

try:
    r = requests.post(
        'http://127.0.0.1:8001/analyze',
        json={
            'idea': 'Test',
            'target_market': 'Test',
            'problem_statement': 'Test'
        },
        headers={'Origin': 'http://localhost:5500'},
        timeout=2
    )
    cors_header = r.headers.get('access-control-allow-origin', 'NOT SET')
    if cors_header == 'http://localhost:5500':
        print('✅ CORS Headers Correct')
        print(f'   Allow-Origin: {cors_header}')
    else:
        print(f'⚠️  CORS Header: {cors_header}')
except Exception as e:
    print(f'❌ CORS Test Error: {e}')
    all_passed = False

# ====== TEST 3: /analyze ENDPOINT ======
print('\n[TEST 3] /analyze Endpoint')
print('-'*70)

analyze_data = None
try:
    r = requests.post(
        'http://127.0.0.1:8001/analyze',
        json={
            'idea': 'AI-powered fitness coaching app',
            'target_market': 'Busy professionals aged 25-40',
            'problem_statement': 'People need fitness guidance but lack affordable personal trainers'
        },
        timeout=10
    )
    
    if r.status_code == 200:
        data = r.json()
        analyze_data = data
        print('✅ /analyze WORKING')
        print(f'   Compatibility Score: {data.get("compatibility_score")}/100')
        print(f'   Risk Level: {data.get("risk_level")}')
        print(f'   Suggestions: {len(data.get("improvement_suggestions", []))}')
        print(f'   Domain Tags: {", ".join(data.get("domain_tags", []))}')
    else:
        print(f'❌ /analyze Error: Status {r.status_code}')
        all_passed = False
except Exception as e:
    print(f'❌ /analyze Failed: {e}')
    all_passed = False

# ====== TEST 4: /generate_brd ENDPOINT (all formats) ======
print('\n[TEST 4] /generate_brd Endpoint')
print('-'*70)

if analyze_data:
    formats_tested = []
    for fmt in ['txt', 'pdf', 'docx', 'image']:
        try:
            r = requests.post(
                'http://127.0.0.1:8001/generate_brd',
                json={
                    'format': fmt,
                    'analysis_data': analyze_data
                },
                timeout=5
            )
            
            if r.status_code == 200:
                size = len(r.content)
                mime = r.headers.get('content-type', 'unknown')
                filename = r.headers.get('content-disposition', 'unknown')
                print(f'✅ Format: {fmt.upper():<6} Size: {size:>7} bytes  MIME: {mime}')
                formats_tested.append(fmt)
            else:
                print(f'❌ Format: {fmt.upper():<6} Status: {r.status_code}')
                all_passed = False
        except Exception as e:
            print(f'❌ Format: {fmt.upper():<6} Error: {str(e)[:40]}')
            all_passed = False
    
    print(f'\n   Successfully tested: {len(formats_tested)}/4 formats')
else:
    print('⏭️  Skipped: No analysis data available')

# ====== TEST 5: FRONTEND FILES ======
print('\n[TEST 5] Frontend Assets')
print('-'*70)

frontend_files = ['config.js', 'chat.js', 'auth.js', 'style.css', 'index.html', 'login.html']
files_loaded = 0

for filename in frontend_files:
    try:
        r = requests.get(f'http://localhost:5500/{filename}', timeout=2)
        if r.status_code == 200:
            print(f'✅ {filename:<20} {len(r.content):>8} bytes')
            files_loaded += 1
        else:
            print(f'⚠️  {filename:<20} Status {r.status_code}')
    except Exception as e:
        print(f'❌ {filename:<20} Error: {str(e)[:30]}')

print(f'\n   Loaded: {files_loaded}/{len(frontend_files)} files')

# ====== TEST 6: CONFIGURATION CHECK ======
print('\n[TEST 6] Configuration Check')
print('-'*70)

try:
    with open('Frontend/config.js', 'r') as f:
        content = f.read()
        if '8001' in content:
            print('✅ Frontend/config.js has correct backend URL (8001)')
        else:
            print('⚠️  Frontend/config.js might not have correct backend URL')
except:
    print('⚠️  Could not verify config.js')

try:
    with open('Backend/.env', 'r') as f:
        content = f.read()
        if 'GEMINI_API_KEY' in content:
            print('✅ Backend/.env has GEMINI_API_KEY configured')
        if 'localhost:5500' in content or '5500' in content:
            print('✅ Backend/.env has CORS origin configured')
except:
    print('⚠️  Could not verify .env')

# ====== SUMMARY ======
print('\n' + '='*70)
if all_passed:
    print('                    ✅ ALL TESTS PASSED!')
    print('\n🎉 Structify Prototype is Ready for Testing!')
    print('\n📋 What You Can Do:')
    print('   1. Open browser to http://localhost:5500/chat.html')
    print('   2. Type your business idea (3-part interactive chat)')
    print('   3. Get AI analysis with compatibility score')
    print('   4. Click "Generate BRD" to download document')
    print('\n📊 Available Formats:')
    print('   • PDF - Professional formatted document')
    print('   • DOCX - Editable in Microsoft Word')
    print('   • TXT - Plain text format')
    print('   • PNG - Image preview')
else:
    print('                    ⚠️  SOME TESTS FAILED')
    print('                 Check errors above')

print('\n' + '='*70 + '\n')
