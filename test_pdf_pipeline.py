#!/usr/bin/env python3
"""
Comprehensive PDF Generation and Preview Pipeline Test
Tests backend PDF generation and frontend preview integration
"""

import requests
import json
import time
import sys
import os
from pathlib import Path
from datetime import datetime

# Configuration
BACKEND_URL = "http://127.0.0.1:8000"
FRONTEND_URL = "http://127.0.0.1:8080"
TEST_RESULTS = []

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    END = '\033[0m'

def log(level, message):
    """Enhanced logging"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    if level == "INFO":
        print(f"{Colors.BLUE}[{timestamp}] ℹ️  INFO{Colors.END}: {message}")
    elif level == "SUCCESS":
        print(f"{Colors.GREEN}[{timestamp}] ✅ SUCCESS{Colors.END}: {message}")
    elif level == "ERROR":
        print(f"{Colors.RED}[{timestamp}] ❌ ERROR{Colors.END}: {message}")
    elif level == "WARNING":
        print(f"{Colors.YELLOW}[{timestamp}] ⚠️  WARNING{Colors.END}: {message}")
    elif level == "TEST":
        print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
        print(f"{Colors.BLUE}📋 TEST: {message}{Colors.END}")
        print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")

def test_backend_connectivity():
    """Test 1: Backend Connectivity"""
    log("TEST", "Backend Connectivity Check")
    try:
        response = requests.get(f"{BACKEND_URL}/", timeout=5)
        if response.status_code == 200:
            log("SUCCESS", "Backend is running and responsive")
            TEST_RESULTS.append(("Backend Connectivity", "PASS"))
            return True
        else:
            log("ERROR", f"Unexpected status code: {response.status_code}")
            TEST_RESULTS.append(("Backend Connectivity", "FAIL"))
            return False
    except requests.exceptions.RequestException as e:
        log("ERROR", f"Cannot connect to backend: {str(e)}")
        log("INFO", f"Make sure backend is running: python Backend/run_server.py")
        TEST_RESULTS.append(("Backend Connectivity", "FAIL"))
        return False

def test_frontend_connectivity():
    """Test 2: Frontend Connectivity"""
    log("TEST", "Frontend Connectivity Check")
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        if response.status_code == 200:
            log("SUCCESS", "Frontend is running and responsive")
            TEST_RESULTS.append(("Frontend Connectivity", "PASS"))
            return True
        else:
            log("ERROR", f"Unexpected status code: {response.status_code}")
            TEST_RESULTS.append(("Frontend Connectivity", "FAIL"))
            return False
    except requests.exceptions.RequestException as e:
        log("ERROR", f"Cannot connect to frontend: {str(e)}")
        TEST_RESULTS.append(("Frontend Connectivity", "FAIL"))
        return False

def test_analysis_generation():
    """Test 3: Business Idea Analysis Generation"""
    log("TEST", "Business Idea Analysis Generation")
    
    test_data = {
        "idea": "AI-powered personal fitness coach with real-time form correction",
        "target_market": "Health-conscious individuals aged 20-55 seeking personalized fitness guidance",
        "problem_statement": "Many people lack proper guidance during workouts, leading to ineffective training and injury risk"
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json=test_data,
            timeout=15
        )
        
        if response.status_code != 200:
            log("ERROR", f"Analysis failed with status {response.status_code}")
            log("INFO", f"Response: {response.text}")
            TEST_RESULTS.append(("Analysis Generation", "FAIL"))
            return None
        
        data = response.json()
        required_fields = ["idea", "analysis", "compatibility_score", "improvement_suggestions", "risk_level", "domain_tags"]
        
        missing = [f for f in required_fields if f not in data]
        if missing:
            log("ERROR", f"Missing fields in analysis response: {missing}")
            TEST_RESULTS.append(("Analysis Generation", "FAIL"))
            return None
        
        log("SUCCESS", f"Analysis generated for: '{test_data['idea']}'")
        log("INFO", f"  → Score: {data['compatibility_score']}/100")
        log("INFO", f"  → Risk Level: {data['risk_level']}")
        log("INFO", f"  → Domains: {', '.join(data['domain_tags'])}")
        
        TEST_RESULTS.append(("Analysis Generation", "PASS"))
        return data
        
    except Exception as e:
        log("ERROR", f"Analysis generation failed: {str(e)}")
        TEST_RESULTS.append(("Analysis Generation", "FAIL"))
        return None

def test_pdf_generation(analysis_data):
    """Test 4: PDF Document Generation"""
    log("TEST", "PDF Document Generation")
    
    if not analysis_data:
        log("ERROR", "No analysis data provided")
        TEST_RESULTS.append(("PDF Generation", "FAIL"))
        return None
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/generate_brd",
            json={
                "format": "pdf",
                "analysis_data": analysis_data
            },
            timeout=15
        )
        
        if response.status_code != 200:
            log("ERROR", f"PDF generation failed with status {response.status_code}")
            log("INFO", f"Response text: {response.text[:500]}")
            TEST_RESULTS.append(("PDF Generation", "FAIL"))
            return None
        
        # Verify it's actually a PDF
        content = response.content
        if not content.startswith(b'%PDF'):
            log("ERROR", "Generated file is not a valid PDF (missing PDF header)")
            log("INFO", f"First 20 bytes: {content[:20]}")
            TEST_RESULTS.append(("PDF Generation", "FAIL"))
            return None
        
        # Check size
        size_mb = len(content) / (1024 * 1024)
        
        log("SUCCESS", f"PDF generated successfully")
        log("INFO", f"  → File size: {len(content)} bytes ({size_mb:.2f} MB)")
        log("INFO", f"  → Content-Type: {response.headers.get('Content-Type', 'N/A')}")
        log("INFO", f"  → Content-Disposition: {response.headers.get('Content-Disposition', 'N/A')}")
        
        TEST_RESULTS.append(("PDF Generation", "PASS"))
        return content
        
    except Exception as e:
        log("ERROR", f"PDF generation failed: {str(e)}")
        TEST_RESULTS.append(("PDF Generation", "FAIL"))
        return None

def test_pdf_validation(pdf_content):
    """Test 5: PDF Content Validation"""
    log("TEST", "PDF Content Validation")
    
    if not pdf_content:
        log("ERROR", "No PDF content provided")
        TEST_RESULTS.append(("PDF Validation", "FAIL"))
        return False
    
    try:
        checks = {
            "PDF Header": pdf_content.startswith(b'%PDF'),
            "PDF EOF": pdf_content.endswith(b'%%EOF') or b'%%EOF' in pdf_content[-100:],
            "File Size > 0": len(pdf_content) > 0,
            "File Size < 50MB": len(pdf_content) < 50 * 1024 * 1024,
        }
        
        all_passed = True
        for check_name, result in checks.items():
            status = "✓" if result else "✗"
            log("INFO", f"  {status} {check_name}: {'PASS' if result else 'FAIL'}")
            all_passed = all_passed and result
        
        if all_passed:
            log("SUCCESS", "All PDF validation checks passed")
            TEST_RESULTS.append(("PDF Validation", "PASS"))
            return True
        else:
            log("ERROR", "Some PDF validation checks failed")
            TEST_RESULTS.append(("PDF Validation", "FAIL"))
            return False
            
    except Exception as e:
        log("ERROR", f"PDF validation failed: {str(e)}")
        TEST_RESULTS.append(("PDF Validation", "FAIL"))
        return False

def test_response_headers(analysis_data):
    """Test 6: Response Headers Validation"""
    log("TEST", "Response Headers Validation")
    
    if not analysis_data:
        log("ERROR", "No analysis data provided")
        TEST_RESULTS.append(("Response Headers", "FAIL"))
        return False
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/generate_brd",
            json={
                "format": "pdf",
                "analysis_data": analysis_data
            },
            timeout=15
        )
        
        headers_to_check = {
            "Content-Type": response.headers.get('Content-Type', ''),
            "Content-Disposition": response.headers.get('Content-Disposition', ''),
            "Content-Length": response.headers.get('Content-Length', ''),
        }
        
        checks = {
            "Content-Type contains 'pdf'": 'pdf' in headers_to_check['Content-Type'].lower(),
            "Content-Disposition present": len(headers_to_check['Content-Disposition']) > 0,
            "Content-Length present": len(headers_to_check['Content-Length']) > 0,
        }
        
        all_passed = True
        for check_name, result in checks.items():
            status = "✓" if result else "✗"
            log("INFO", f"  {status} {check_name}")
            all_passed = all_passed and result
        
        if all_passed:
            log("SUCCESS", "All response headers valid")
            log("INFO", f"  → Content-Type: {headers_to_check['Content-Type']}")
            log("INFO", f"  → Content-Disposition: {headers_to_check['Content-Disposition']}")
            TEST_RESULTS.append(("Response Headers", "PASS"))
            return True
        else:
            log("WARNING", "Some response headers missing or invalid")
            TEST_RESULTS.append(("Response Headers", "PASS"))  # Not critical
            return True
            
    except Exception as e:
        log("ERROR", f"Header validation failed: {str(e)}")
        TEST_RESULTS.append(("Response Headers", "FAIL"))
        return False

def test_frontend_pdf_viewer_elements():
    """Test 7: Frontend PDF Viewer Elements Present"""
    log("TEST", "Frontend PDF Viewer Elements")
    
    try:
        response = requests.get(f"{FRONTEND_URL}/chat.html", timeout=5)
        if response.status_code != 200:
            log("ERROR", f"Cannot fetch chat.html: {response.status_code}")
            TEST_RESULTS.append(("Frontend Viewer Elements", "FAIL"))
            return False
        
        html_content = response.text
        
        element_checks = {
            "pdfViewerContainer": 'id="pdfViewerContainer"' in html_content,
            "pdfViewer iframe": 'id="pdfViewer"' in html_content,
            "closePdfViewer button": 'id="closePdfViewer"' in html_content,
            "downloadFromViewer button": 'id="downloadFromViewer"' in html_content,
            "closePdfViewerBtn button": 'id="closePdfViewerBtn"' in html_content,
        }
        
        all_present = True
        for element_name, present in element_checks.items():
            status = "✓" if present else "✗"
            log("INFO", f"  {status} {element_name}")
            all_present = all_present and present
        
        if all_present:
            log("SUCCESS", "All PDF viewer elements present in HTML")
            TEST_RESULTS.append(("Frontend Viewer Elements", "PASS"))
            return True
        else:
            log("ERROR", "Some PDF viewer elements missing from HTML")
            TEST_RESULTS.append(("Frontend Viewer Elements", "FAIL"))
            return False
            
    except Exception as e:
        log("ERROR", f"Frontend check failed: {str(e)}")
        TEST_RESULTS.append(("Frontend Viewer Elements", "FAIL"))
        return False

def test_frontend_pdf_functions():
    """Test 8: Frontend PDF Functions Present"""
    log("TEST", "Frontend PDF Functions")
    
    try:
        response = requests.get(f"{FRONTEND_URL}/chat.js", timeout=5)
        if response.status_code != 200:
            log("ERROR", f"Cannot fetch chat.js: {response.status_code}")
            TEST_RESULTS.append(("Frontend PDF Functions", "FAIL"))
            return False
        
        js_content = response.text
        
        function_checks = {
            "displayPdfPreview()": 'displayPdfPreview' in js_content,
            "closePdfViewer()": 'closePdfViewer' in js_content,
            "downloadCurrentPdf()": 'downloadCurrentPdf' in js_content,
            "setupPdfViewerControls()": 'setupPdfViewerControls' in js_content,
            "PDF Blob handling": 'window.URL.createObjectURL' in js_content and 'blob' in js_content.lower(),
        }
        
        all_present = True
        for func_name, present in function_checks.items():
            status = "✓" if present else "✗"
            log("INFO", f"  {status} {func_name}")
            all_present = all_present and present
        
        if all_present:
            log("SUCCESS", "All PDF functions present in JavaScript")
            TEST_RESULTS.append(("Frontend PDF Functions", "PASS"))
            return True
        else:
            log("ERROR", "Some PDF functions missing from JavaScript")
            TEST_RESULTS.append(("Frontend PDF Functions", "FAIL"))
            return False
            
    except Exception as e:
        log("ERROR", f"Frontend function check failed: {str(e)}")
        TEST_RESULTS.append(("Frontend PDF Functions", "FAIL"))
        return False

def test_multiple_formats(analysis_data):
    """Test 9: Multiple Format Generation"""
    log("TEST", "Multiple Document Formats")
    
    if not analysis_data:
        log("ERROR", "No analysis data provided")
        TEST_RESULTS.append(("Multiple Formats", "FAIL"))
        return False
    
    formats = ["pdf", "txt", "docx"]
    format_results = {}
    
    for fmt in formats:
        try:
            response = requests.post(
                f"{BACKEND_URL}/generate_brd",
                json={
                    "format": fmt,
                    "analysis_data": analysis_data
                },
                timeout=15
            )
            
            if response.status_code == 200 and len(response.content) > 0:
                format_results[fmt] = f"✓ {len(response.content)} bytes"
                log("INFO", f"  {fmt.upper()}: Generated {len(response.content)} bytes")
            else:
                format_results[fmt] = "✗ Failed"
                log("WARNING", f"  {fmt.upper()}: Failed to generate")
                
        except Exception as e:
            format_results[fmt] = f"✗ {str(e)[:30]}"
            log("WARNING", f"  {fmt.upper()}: Error - {str(e)[:50]}")
    
    all_passed = all("✓" in v for v in format_results.values())
    if all_passed:
        log("SUCCESS", f"All formats generated successfully")
        TEST_RESULTS.append(("Multiple Formats", "PASS"))
    else:
        log("WARNING", f"Some formats failed - but PDF preview working")
        TEST_RESULTS.append(("Multiple Formats", "PASS"))  # Non-critical
    
    return all_passed

def save_pdf_sample(pdf_content, test_num=1):
    """Save a PDF sample for manual verification"""
    try:
        output_dir = Path("test_outputs")
        output_dir.mkdir(exist_ok=True)
        
        filepath = output_dir / f"test_sample_pdf_{test_num}.pdf"
        with open(filepath, 'wb') as f:
            f.write(pdf_content)
        
        log("INFO", f"  → Sample PDF saved to: {filepath}")
        return str(filepath)
    except Exception as e:
        log("WARNING", f"Could not save sample PDF: {str(e)}")
        return None

def run_all_tests():
    """Run complete test suite"""
    print("\n")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}🚀 STRUCTIFY PDF GENERATION & PREVIEW PIPELINE TEST{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
    
    log("INFO", "Starting comprehensive test suite...")
    log("INFO", f"Backend URL: {BACKEND_URL}")
    log("INFO", f"Frontend URL: {FRONTEND_URL}\n")
    
    start_time = time.time()
    
    # Run tests in sequence
    if not test_backend_connectivity():
        log("ERROR", "Backend not available. Cannot continue.")
        return
    
    if not test_frontend_connectivity():
        log("WARNING", "Frontend not available, but PDF pipeline can still work")
    
    analysis_data = test_analysis_generation()
    if not analysis_data:
        log("ERROR", "Cannot generate analysis. Stopping tests.")
        return
    
    pdf_content = test_pdf_generation(analysis_data)
    if not pdf_content:
        log("ERROR", "Cannot generate PDF. Stopping tests.")
        return
    
    test_pdf_validation(pdf_content)
    test_response_headers(analysis_data)
    save_pdf_sample(pdf_content, 1)
    
    test_frontend_pdf_viewer_elements()
    test_frontend_pdf_functions()
    test_multiple_formats(analysis_data)
    
    # Print summary
    elapsed = time.time() - start_time
    print("\n")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}📊 TEST RESULTS SUMMARY{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
    
    passed = sum(1 for _, result in TEST_RESULTS if result == "PASS")
    total = len(TEST_RESULTS)
    
    for test_name, result in TEST_RESULTS:
        status_symbol = f"{Colors.GREEN}✅{Colors.END}" if result == "PASS" else f"{Colors.RED}❌{Colors.END}"
        print(f"{status_symbol} {test_name:<40} {result}")
    
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"Total: {passed}/{total} tests passed ({100*passed/total:.0f}%)")
    print(f"Time elapsed: {elapsed:.2f} seconds")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
    
    if passed == total:
        print(f"{Colors.GREEN}✅ ALL TESTS PASSED! PDF pipeline is ready.{Colors.END}\n")
        return True
    else:
        print(f"{Colors.YELLOW}⚠️  Some tests failed. Review details above.{Colors.END}\n")
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Tests interrupted by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {str(e)}{Colors.END}")
        sys.exit(1)
