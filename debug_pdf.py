#!/usr/bin/env python3
import requests
import json

test_data = {
    'idea': 'AI-powered personal fitness coach with real-time form correction',
    'target_market': 'Health-conscious individuals aged 20-55 seeking personalized fitness guidance',
    'problem_statement': 'Many people lack proper guidance during workouts, leading to ineffective training and injury risk'
}

# Get analysis first
print('Getting analysis...')
response = requests.post('http://127.0.0.1:8000/analyze', json=test_data)
analysis = response.json()
print(f'Analysis received: {analysis.get("compatibility_score")}')

# Try to generate PDF
print('\nGenerating PDF...')
response = requests.post('http://127.0.0.1:8000/generate_brd', json={
    'format': 'pdf',
    'analysis_data': analysis
})

print(f'Status: {response.status_code}')
print(f'Content-Type: {response.headers.get("Content-Type")}')
print(f'Content length: {len(response.content)}')
print(f'First 100 bytes: {response.content[:100]}')
print(f'Is PDF: {response.content.startswith(b"%PDF")}')
print(f'\nFull content first 500 chars:')
print(response.content[:500])
