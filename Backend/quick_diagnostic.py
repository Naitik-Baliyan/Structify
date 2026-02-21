#!/usr/bin/env python3
"""Quick diagnostic test for Structify prototype"""

import requests
import sys

print('🔍 STRUCTIFY PROTOTYPE DIAGNOSTIC')
print('='*60)

all_ok = True

# Test 1: Backend health
print('\n[1/3] Backend Health Check')
print('-'*60)
try:
    response = requests.get('http://127.0.0.1:8001/', timeout=2)
    if response.status_code == 200:
        print('✅ Backend is RUNNING on http://127.0.0.1:8001')
    else:
        print(f'❌ Backend returned status {response.status_code}')
        all_ok = False
except Exception as e:
    print(f'❌ Backend NOT ACCESSIBLE: {e}')
    all_ok = False

# Test 2: Analyze endpoint
print('\n[2/3] Testing /analyze Endpoint')
print('-'*60)
try:
    response = requests.post('http://127.0.0.1:8001/analyze', json={
        'idea': 'AI-powered fitness coaching app',
        'target_market': 'Busy professionals aged 25-40',
        'problem_statement': 'People need professional fitness guidance but lack time for trainers'
    }, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        score = data.get('compatibility_score', 'N/A')
        risk = data.get('risk_level', 'N/A')
        tags = data.get('domain_tags', [])
        print('✅ /analyze endpoint WORKING')
        print(f'   • Compatibility Score: {score}/100')
        print(f'   • Risk Level: {risk}')
        print(f'   • Domain Tags: {", ".join(tags) if tags else "N/A"}')
    else:
        print(f'❌ /analyze returned status {response.status_code}')
        print(f'   Response: {response.text[:150]}')
        all_ok = False
except Exception as e:
    print(f'❌ /analyze ERROR: {e}')
    all_ok = False

# Test 3: BRD endpoint
print('\n[3/3] Testing /generate_brd Endpoint')
print('-'*60)
try:
    response = requests.post('http://127.0.0.1:8001/generate_brd', json={
        'format': 'txt',
        'analysis_data': {
            'idea': 'AI fitness coaching app',
            'target_market': 'Busy professionals',
            'problem_statement': 'Need fitness guidance without personal trainer',
            'analysis': 'Strong market opportunity with growing demand for AI fitness solutions',
            'compatibility_score': 72,
            'improvement_suggestions': ['Market research', 'MVP development', 'Partnership strategy'],
            'risk_level': 'medium',
            'domain_tags': ['tech', 'health', 'fitness']
        }
    }, timeout=5)
    
    if response.status_code == 200:
        file_size = len(response.content)
        print('✅ /generate_brd endpoint WORKING')
        print(f'   • Generated {file_size} bytes')
        print(f'   • Format: TXT (text/plain)')
        print(f'   • File: BRD_AI_fitness_coaching_app.txt')
    else:
        print(f'❌ /generate_brd returned status {response.status_code}')
        print(f'   Response: {response.text[:150]}')
        all_ok = False
except Exception as e:
    print(f'❌ /generate_brd ERROR: {e}')
    all_ok = False

# Summary
print('\n' + '='*60)
if all_ok:
    print('✅ ALL TESTS PASSED - Prototype is working correctly!')
    print('\n💡 To use locally:')
    print('   1. Frontend should be running on http://localhost:5500')
    print('   2. Backend is running on http://127.0.0.1:8001')
    print('   3. Check Frontend/config.js has BACKEND_URL = "http://127.0.0.1:8001"')
    sys.exit(0)
else:
    print('❌ SOME TESTS FAILED - See details above')
    print('\n🔧 Troubleshooting:')
    print('   • Backend running? python -m uvicorn main:app --host 127.0.0.1 --port 8000')
    print('   • Wrong port? Update Frontend/config.js BACKEND_URL')
    print('   • Connection issue? Check firewall, network settings')
    sys.exit(1)
