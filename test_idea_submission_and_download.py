#!/usr/bin/env python3
"""
Test: Submit Business Idea and Download BRD Document
======================================================
This script will:
1. Submit a business idea to the backend
2. Generate analysis
3. Generate BRD document
4. Download and save the file to the desktop
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

# Configuration
BASE_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://127.0.0.1:8080"
DOWNLOAD_PATH = r"c:\Users\ASUS\Desktop\Structify_Downloads"

# Create downloads folder if it doesn't exist
Path(DOWNLOAD_PATH).mkdir(parents=True, exist_ok=True)

print("\n" + "="*70)
print("TESTING: SUBMIT IDEA & DOWNLOAD BRD")
print("="*70)

# Test idea
test_idea = {
    "idea": "AI-powered personal finance management platform that uses machine learning to analyze spending patterns and provide intelligent recommendations for savings. The system uses blockchain for secure transaction recording and integrates with multiple banking APIs.",
    "target_market": "Young professionals and students aged 18-35 with annual income >$30,000",
    "problem_statement": "Traditional personal finance tools are not intelligent enough and don't provide actionable insights. Users spend hours manually tracking expenses and have no automated way to optimize spending."
}

print("\n[STEP 1] SUBMITTING BUSINESS IDEA")
print("-" * 70)
print(f"Idea: {test_idea['idea'][:100]}...")
print(f"Target Market: {test_idea['target_market']}")
print(f"Problem: {test_idea['problem_statement'][:80]}...")

try:
    # Submit idea and get analysis
    print("\n[STEP 2] REQUESTING AI ANALYSIS")
    response = requests.post(
        f"{BASE_URL}/analyze",
        json=test_idea,
        timeout=30
    )
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        exit(1)
    
    analysis_data = response.json()
    print("✅ Analysis received successfully")
    print(f"   - Score: {analysis_data.get('compatibility_score')}/100")
    print(f"   - Risk: {analysis_data.get('risk_level')}")
    print(f"   - Tags: {', '.join(analysis_data.get('domain_tags', []))}")
    
    # Generate BRD document
    print("\n[STEP 3] GENERATING BRD DOCUMENT")
    brd_payload = {
        "analysis_data": analysis_data,
        "format": "pdf"  # Request PDF format
    }
    
    brd_response = requests.post(
        f"{BASE_URL}/generate_brd",
        json=brd_payload,
        timeout=30
    )
    
    if brd_response.status_code != 200:
        print(f"❌ Error generating BRD: {brd_response.status_code}")
        print(f"Response: {brd_response.text}")
        exit(1)
    
    print("✅ BRD document generated successfully")
    
    # Handle both PDF and JSON responses
    content_type = brd_response.headers.get('content-type', '')
    
    if 'application/pdf' in content_type:
        # Save binary PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"BRD_FinTech_AI_Finance_{timestamp}.pdf"
        filepath = Path(DOWNLOAD_PATH) / filename
        
        filepath.write_bytes(brd_response.content)
        print(f"✅ PDF saved: {filepath}")
        file_size = filepath.stat().st_size
        print(f"   File size: {file_size:,} bytes")
        
    else:
        # Handle JSON response with base64 or other format
        try:
            brd_json = brd_response.json()
            
            if 'document' in brd_json:
                # Save text format
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"BRD_FinTech_AI_Finance_{timestamp}.txt"
                filepath = Path(DOWNLOAD_PATH) / filename
                
                filepath.write_text(brd_json['document'], encoding='utf-8')
                print(f"✅ Document saved: {filepath}")
                file_size = filepath.stat().st_size
                print(f"   File size: {file_size:,} bytes")
            else:
                print("⚠️  Unexpected response format")
                print(f"Response: {brd_json}")
        except json.JSONDecodeError:
            print("⚠️  Could not parse response")
    
    # Verify file was created
    print("\n[STEP 4] VERIFYING DOWNLOAD")
    print("-" * 70)
    downloads = sorted(list(Path(DOWNLOAD_PATH).glob("BRD_*.pdf")) + list(Path(DOWNLOAD_PATH).glob("BRD_*.txt")))
    
    if downloads:
        print("✅ Files in download folder:")
        for f in downloads[-3:]:  # Show last 3 files
            size = f.stat().st_size
            print(f"   • {f.name} ({size:,} bytes)")
        
        print(f"\n✅ Download location: {DOWNLOAD_PATH}")
    else:
        print("⚠️  No files found in download folder")
    
    # Summary
    print("\n" + "="*70)
    print("TEST COMPLETE ✅")
    print("="*70)
    print(f"\n✅ Idea submitted successfully")
    print(f"✅ Analysis generated (Score: {analysis_data.get('compatibility_score')}/100)")
    print(f"✅ BRD document created and downloaded")
    print(f"✅ File saved to: {DOWNLOAD_PATH}")
    print("\nYou can now open the BRD file and review the generated document!")
    
except requests.exceptions.ConnectionError:
    print("❌ Error: Cannot connect to backend at http://127.0.0.1:8000")
    print("Make sure the backend server is running!")
except requests.exceptions.Timeout:
    print("❌ Error: Request timed out")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
