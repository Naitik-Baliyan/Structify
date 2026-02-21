#!/usr/bin/env python3
"""
Structify Backend Testing Script
================================

Simple tool to test the Structify backend API without curl.
Usage: python test_api.py
"""

import requests
import json
import sys
from typing import Dict, Any

BASE_URL = "http://127.0.0.1:8001"

def print_section(title: str) -> None:
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def print_response(response: requests.Response) -> None:
    """Pretty print a response"""
    print(f"Status Code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
    print("\nResponse Body:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_health_check() -> bool:
    """Test the health check endpoint"""
    print_section("Health Check Test")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print_response(response)
        
        if response.status_code == 200:
            print("\n✅ Health check passed!")
            return True
        else:
            print("\n❌ Health check failed!")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure backend is running: python -m uvicorn main:app --reload")
        return False

def test_analysis(payload: Dict[str, str]) -> tuple:
    """Test the analysis endpoint, returns (success, analysis_data)"""
    print_section("Analysis Test")
    
    print("Request Payload:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Analysis successful!")
            print(f"  Compatibility Score: {data.get('compatibility_score')}/100")
            print(f"  Risk Level: {data.get('risk_level')}")
            print(f"  Suggestions: {len(data.get('improvement_suggestions', []))}")
            print(f"  Domain Tags: {', '.join(data.get('domain_tags', []))}")
            return True, data
        else:
            print("\n❌ Analysis request failed!")
            return False, None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, None

def test_validation() -> bool:
    """Test input validation"""
    print_section("Input Validation Test")
    
    print("Testing with empty fields...")
    payload = {
        "idea": "",
        "target_market": "",
        "problem_statement": ""
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print_response(response)
        
        if response.status_code == 400:
            print("\n✅ Validation check passed!")
            return True
        else:
            print("\n❌ Validation check failed!")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_brd_generation(analysis_data: Dict[str, Any]) -> bool:
    """Test BRD generation endpoint with different formats"""
    print_section("BRD Generation Test")
    
    formats_to_test = ["txt", "pdf", "docx", "image"]
    results = []
    
    for format_type in formats_to_test:
        print(f"\nTesting format: {format_type.upper()}")
        print("-" * 40)
        
        try:
            payload = {
                "format": format_type,
                "analysis_data": analysis_data
            }
            
            response = requests.post(
                f"{BASE_URL}/generate_brd",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Content-Type: {response.headers.get('Content-Type', 'N/A')}")
            
            if response.status_code == 200:
                # Check if response contains file content
                content_length = len(response.content)
                print(f"Document Size: {content_length} bytes")
                
                # Verify Content-Disposition header
                disposition = response.headers.get('Content-Disposition', '')
                if disposition:
                    print(f"Download Filename: {disposition.split('filename=')[-1]}")
                    results.append((format_type, True))
                    print(f"✅ {format_type.upper()} generation successful!")
                else:
                    print(f"⚠️  Missing Content-Disposition header")
                    results.append((format_type, False))
            else:
                print(f"Response: {response.text[:200]}")
                results.append((format_type, False))
                print(f"❌ {format_type.upper()} generation failed!")
                
        except Exception as e:
            print(f"❌ Error testing {format_type}: {str(e)}")
            results.append((format_type, False))
    
    # Summary
    print("\n" + "="*40)
    successful = sum(1 for _, success in results if success)
    print(f"BRD Generation Summary: {successful}/{len(results)} formats successful")
    
    return successful > 0

def run_demo_analysis() -> None:
    """Run a demo analysis with sample data"""
    print_section("Demo Analysis: AI-Powered Fitness Coach")
    
    payload = {
        "idea": "AI-powered personal fitness coach app with real-time form correction",
        "target_market": "Busy professionals aged 25-40 who want gym guidance at home",
        "problem_statement": "People don't have time for personal trainers but need professional fitness guidance and real-time feedback to avoid injuries"
    }
    
    test_analysis(payload)

def run_all_tests() -> None:
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  Structify Backend API Test Suite".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    results = []
    analysis_data = None
    
    # Test 1: Health Check
    print("\n[1/5] Running health check test...")
    results.append(("Health Check", test_health_check()))
    
    if not results[-1][1]:
        print("\n⚠️  Backend not running. Cannot continue tests.")
        return
    
    # Test 2: Validation
    print("\n[2/5] Running validation test...")
    results.append(("Input Validation", test_validation()))
    
    # Test 3: Demo Analysis
    print("\n[3/5] Running demo analysis...")
    success, analysis_data = test_analysis({
        "idea": "AI-powered fitness coach app",
        "target_market": "Busy professionals",
        "problem_statement": "People need gym guidance but lack time for trainers"
    })
    results.append(("Demo Analysis", success))
    
    # Test 4: Real-world Example
    print("\n[4/5] Running real-world example...")
    success, analysis_data = test_analysis({
        "idea": "Blockchain-based supply chain transparency platform",
        "target_market": "Fortune 500 manufacturing and retail companies",
        "problem_statement": "Companies struggle with counterfeit products and supply chain visibility due to fragmented data systems"
    })
    results.append(("Real-world Analysis", success))
    
    # Test 5: BRD Generation (if we have analysis data)
    print("\n[5/5] Running BRD generation tests...")
    if analysis_data:
        brd_success = test_brd_generation(analysis_data)
        results.append(("BRD Generation", brd_success))
    else:
        print("⚠️  Skipping BRD generation test - no analysis data available")
        results.append(("BRD Generation", False))
    
    # Summary
    print_section("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print()
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {test_name}")
    
    print()
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Check the output above.")

def main() -> None:
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "health":
            test_health_check()
        elif command == "validate":
            test_validation()
        elif command == "demo":
            run_demo_analysis()
        elif command == "all":
            run_all_tests()
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
    else:
        run_all_tests()

def print_help() -> None:
    """Print help information"""
    print("""
Usage: python test_api.py [COMMAND]

Commands:
  health    - Test health check endpoint
  validate  - Test input validation
  demo      - Run demo analysis
  all       - Run complete test suite (default)

Examples:
  python test_api.py              # Run all tests
  python test_api.py health       # Check if backend is running
  python test_api.py demo         # Run a demo analysis
  python test_api.py validate     # Test input validation

Before running tests:
  1. Start the backend: python -m uvicorn main:app --reload
  2. Install requests: pip install requests
""")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ Tests interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
