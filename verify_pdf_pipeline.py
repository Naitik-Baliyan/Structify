#!/usr/bin/env python3
"""
Quick PDF Pipeline Verification Script
Run this anytime to verify the PDF generation and preview system is working
"""

import requests
import sys
import time

def colored_text(text, color):
    """Return colored terminal text"""
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'end': '\033[0m'
    }
    return f"{colors.get(color, '')}{text}{colors['end']}"

def check_component(name, url, method="GET", expected_status=200):
    """Check if a component is responsive"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=3)
        else:
            response = requests.post(url, json={}, timeout=3)
        
        if response.status_code == expected_status:
            print(f"  {colored_text('✓', 'green')} {name:30} RUNNING")
            return True
        else:
            print(f"  {colored_text('✗', 'red')} {name:30} ({response.status_code})")
            return False
    except Exception as e:
        print(f"  {colored_text('✗', 'red')} {name:30} OFFLINE")
        return False

def verify_file(filepath, name, required_content=None):
    """Verify a file exists and optionally contains specific content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if required_content:
            if required_content.lower() in content.lower():
                print(f"  {colored_text('✓', 'green')} {name:30} FOUND")
                return True
            else:
                print(f"  {colored_text('✗', 'red')} {name:30} NOT FOUND")
                return False
        else:
            print(f"  {colored_text('✓', 'green')} {name:30} EXISTS")
            return True
    except FileNotFoundError:
        print(f"  {colored_text('✗', 'red')} {name:30} MISSING")
        return False
    except Exception as e:
        print(f"  {colored_text('✗', 'red')} {name:30} ERROR: {str(e)}")
        return False

def test_pdf_generation():
    """Test actual PDF generation"""
    print(f"\n{colored_text('Testing PDF Generation...', 'blue')}")
    
    test_data = {
        'idea': 'AI fitness app',
        'target_market': 'Fitness enthusiasts',
        'problem_statement': 'Need better guidance'
    }
    
    try:
        # Get analysis
        response = requests.post(
            'http://127.0.0.1:8000/analyze',
            json=test_data,
            timeout=5
        )
        
        if response.status_code != 200:
            print(f"  {colored_text('✗', 'red')} Analysis generation failed")
            return False
        
        analysis = response.json()
        
        # Generate PDF
        response = requests.post(
            'http://127.0.0.1:8000/generate_brd',
            json={'format': 'pdf', 'analysis_data': analysis},
            timeout=5
        )
        
        if response.status_code != 200:
            print(f"  {colored_text('✗', 'red')} PDF generation failed")
            return False
        
        pdf_data = response.content
        
        if pdf_data.startswith(b'%PDF'):
            size_kb = len(pdf_data) / 1024
            print(f"  {colored_text('✓', 'green')} PDF Generated ({size_kb:.1f} KB)")
            return True
        else:
            print(f"  {colored_text('✗', 'red')} Invalid PDF format")
            return False
            
    except Exception as e:
        print(f"  {colored_text('✗', 'red')} Error: {str(e)}")
        return False

def main():
    print("\n" + "="*70)
    print(colored_text("  STRUCTIFY PDF PIPELINE VERIFICATION", 'blue'))
    print("="*70)
    
    results = {}
    
    # Check System
    print(f"\n{colored_text('Server Status:', 'blue')}")
    results['backend'] = check_component("Backend (.venv)", "http://127.0.0.1:8000/", "GET", 200)
    results['frontend'] = check_component("Frontend (port 8080)", "http://127.0.0.1:8080", "GET", 200)
    
    # Check Dependencies
    print(f"\n{colored_text('Python Dependencies:', 'blue')}")
    results['reportlab'] = verify_file(
        'Backend/requirements.txt',
        'reportlab in requirements',
        'reportlab'
    )
    results['python_docx'] = verify_file(
        'Backend/requirements.txt',
        'python-docx in requirements',
        'python-docx'
    )
    
    # Check Backend Modifications
    print(f"\n{colored_text('Backend Modifications:', 'blue')}")
    results['main_tempfile'] = verify_file(
        'Backend/main.py',
        'Tempfile import added',
        'import tempfile'
    )
    results['main_fileresponse'] = verify_file(
        'Backend/main.py',
        'FileResponse usage',
        'FileResponse'
    )
    results['main_validation'] = verify_file(
        'Backend/main.py',
        'Buffer validation',
        'not document_content or len(document_content) == 0'
    )
    
    # Check Frontend Modifications
    print(f"\n{colored_text('Frontend HTML:', 'blue')}")
    results['html_container'] = verify_file(
        'Frontend/chat.html',
        'pdfViewerContainer div',
        'id="pdfViewerContainer"'
    )
    results['html_iframe'] = verify_file(
        'Frontend/chat.html',
        'pdfViewer iframe',
        'id="pdfViewer"'
    )
    results['html_buttons'] = verify_file(
        'Frontend/chat.html',
        'PDF control buttons',
        'id="closePdfViewer"'
    )
    
    # Check Frontend JavaScript
    print(f"\n{colored_text('Frontend JavaScript:', 'blue')}")
    results['js_displaypdf'] = verify_file(
        'Frontend/chat.js',
        'displayPdfPreview function',
        'function displayPdfPreview'
    )
    results['js_setupcontrols'] = verify_file(
        'Frontend/chat.js',
        'setupPdfViewerControls function',
        'function setupPdfViewerControls'
    )
    results['js_closepdf'] = verify_file(
        'Frontend/chat.js',
        'closePdfViewer function',
        'function closePdfViewer'
    )
    results['js_download'] = verify_file(
        'Frontend/chat.js',
        'downloadCurrentPdf function',
        'function downloadCurrentPdf'
    )
    results['js_bloburl'] = verify_file(
        'Frontend/chat.js',
        'Blob URL handling',
        'window.URL.createObjectURL'
    )
    
    # Test PDF Generation
    if results['backend']:
        results['pdf_gen'] = test_pdf_generation()
    else:
        results['pdf_gen'] = False
        print(f"  {colored_text('⊘', 'yellow')} Skipping PDF generation test (backend offline)")
    
    # Summary
    print(f"\n" + "="*70)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    if passed == total:
        print(colored_text(f"✅ ALL SYSTEMS OPERATIONAL ({passed}/{total})", 'green'))
        print("\nThe PDF generation and preview pipeline is ready for use!")
        return 0
    else:
        print(colored_text(f"⚠️  SOME CHECKS FAILED ({passed}/{total})", 'yellow'))
        print("\nFailed checks:")
        for name, result in results.items():
            if not result:
                print(f"  • {name}")
        return 1
    
if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n{colored_text('Verification interrupted', 'yellow')}")
        sys.exit(1)
