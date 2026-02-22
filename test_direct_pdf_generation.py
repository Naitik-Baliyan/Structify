#!/usr/bin/env python3
import sys
sys.path.insert(0, 'Backend')

from services.brd_generator import BRDExporter, BRDGenerator

# Create sample BRD content
sample_brd = """
================================================================================
STRUCTIFY BUSINESS REQUIREMENTS DOCUMENT (BRD)
================================================================================

1. EXECUTIVE SUMMARY
This is a test BRD document for a fitness application.

2. PROJECT OVERVIEW
A revolutionary fitness coaching platform powered by AI.

3. FEATURES
- Real-time form correction
- Personalized workout plans
- Progress tracking
"""

print("Testing PDF generation...")
print("=" * 50)

try:
    # Test to_pdf method
    exporter = BRDExporter()
    pdf_buffer = exporter.to_pdf(sample_brd)
    
    pdf_content = pdf_buffer.getvalue()
    
    print(f"PDF Content Length: {len(pdf_content)} bytes")
    print(f"First 50 bytes: {pdf_content[:50]}")
    print(f"Is PDF: {pdf_content.startswith(b'%PDF')}")
    
    if pdf_content.startswith(b'%PDF'):
        print("\n✅ SUCCESS: PDF generated correctly!")
        # Save for inspection
        with open('test_direct_pdf.pdf', 'wb') as f:
            f.write(pdf_content)
        print("Saved to test_direct_pdf.pdf")
    else:
        print("\n❌ FAILURE: Not a valid PDF")
        print(f"Content type: {type(pdf_content)}")
        print(f"First 100 chars (decoded): {pdf_content[:100].decode('utf-8', errors='replace')}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
