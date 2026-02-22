#!/usr/bin/env python3
"""
Integration Test for BRD Formatter with Backend Analysis Data

Demonstrates how BRDFormatter works with real analysis data flow
from the analyze endpoint to produce formal BRD documents.
"""

import sys
import os
import json

# Add Backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Backend'))

from services.brd_generator import BRDFormatter, BRDExporter

def test_integration():
    """Test BRD formatter integration with typical backend analysis response"""
    
    # Simulate analysis data from /analyze endpoint
    analysis_data = {
        'idea': 'Enterprise Task Management Platform',
        'target_market': 'Mid-market and Enterprise Organizations (50-5000 employees)',
        'problem_statement': 'Teams struggle with fragmented task management across multiple tools, leading to inefficiency and communication gaps',
        'analysis': 'Market analysis shows strong demand for unified task management solutions. Competitors exist but opportunities for differentiation through superior UX and integrations.',
        'compatibility_score': 82,
        'improvement_suggestions': [
            'Develop partnership program with popular project management integrations',
            'Build comprehensive user onboarding and training program',
            'Establish advisory board with industry leaders',
            'Create data security and compliance certifications'
        ],
        'risk_level': 'medium',
        'domain_tags': ['Enterprise Software', 'SaaS', 'Productivity Tools', 'Team Collaboration']
    }
    
    print("=" * 100)
    print("BRD FORMATTER INTEGRATION TEST - Backend Analysis Data")
    print("=" * 100)
    print()
    
    print("INPUT: Analysis Data (from /analyze endpoint)")
    print("-" * 100)
    print(json.dumps(analysis_data, indent=2))
    print()
    
    # Initialize formatter with analysis data
    formatter = BRDFormatter(analysis_data)
    
    # Generate BRD in markdown format
    brd_markdown = formatter.generate_formatted_brd()
    
    print("OUTPUT: Formal Business Requirements Document")
    print("-" * 100)
    print(brd_markdown)
    print()
    
    # Test section validation
    print("=" * 100)
    print("SECTION VALIDATION")
    print("=" * 100)
    print()
    
    sections = {
        "Header Metadata": [
            "BUSINESS REQUIREMENTS DOCUMENT",
            "Project Name:",
            "Document Status"
        ],
        "Executive Summary": [
            "## 1. Executive Summary",
            "target market",
            "problem"
        ],
        "Project Objectives": [
            "## 2. Project Objectives",
            "Establish market presence",
            "Deliver measurable customer value"
        ],
        "Project Scope": [
            "## 3. Project Scope",
            "IN SCOPE",
            "OUT OF SCOPE"
        ],
        "Business Requirements": [
            "## 4. Business Requirements",
            "| Priority Level | Critical Level | Requirement Description |",
            "System shall"
        ],
        "Key Stakeholders": [
            "## 5. Key Stakeholders",
            "| Name | Job Role | Duties |",
            "Project Manager"
        ],
        "Project Constraints": [
            "## 6. Project Constraints",
            "| Constraint | Description |",
            "Market Dependency"
        ],
        "Cost-Benefit Analysis": [
            "## 7. Cost-Benefit Analysis",
            "| Cost | Benefit |",
            "Financial Projection"
        ]
    }
    
    all_valid = True
    for section_name, keywords in sections.items():
        present = all(keyword in brd_markdown for keyword in keywords)
        status = "[OK]" if present else "[FAIL]"
        print(f"{status} {section_name:<30} ", end="")
        if present:
            print("Valid")
        else:
            print("INVALID - Missing required content")
            all_valid = False
    
    print()
    print("=" * 100)
    
    # Test content consistency with input data
    print("CONTENT CONSISTENCY CHECK")
    print("=" * 100)
    print()
    
    consistency_checks = {
        "Project name included": analysis_data['idea'] in brd_markdown,
        "Target market included": analysis_data['target_market'] in brd_markdown,
        "Problem statement included": analysis_data['problem_statement'] in brd_markdown,
        "Compatibility score used": str(analysis_data['compatibility_score']) in brd_markdown,
        "Domain tags included": any(tag in brd_markdown for tag in analysis_data['domain_tags']),
        "Risk level referenced": analysis_data['risk_level'].upper() in brd_markdown,
    }
    
    for check, result in consistency_checks.items():
        status = "[OK]" if result else "[FAIL]"
        print(f"{status} {check}")
        all_valid = all_valid and result
    
    print()
    print("=" * 100)
    
    # Test export capability
    print("EXPORT FORMAT CAPABILITIES")
    print("=" * 100)
    print()
    
    exporter = BRDExporter()
    
    try:
        txt_buffer = exporter.to_text(brd_markdown)
        txt_size = len(txt_buffer.getvalue())
        print(f"[OK] TXT Export: {txt_size} bytes")
    except Exception as e:
        print(f"[FAIL] TXT Export: {e}")
        all_valid = False
    
    try:
        docx_buffer = exporter.to_docx(brd_markdown)
        docx_size = len(docx_buffer.getvalue())
        print(f"[OK] DOCX Export: {docx_size} bytes")
    except Exception as e:
        print(f"[FAIL] DOCX Export: {e}")
    
    try:
        pdf_buffer = exporter.to_pdf(brd_markdown)
        pdf_size = len(pdf_buffer.getvalue())
        print(f"[OK] PDF Export: {pdf_size} bytes")
    except Exception as e:
        print(f"[FAIL] PDF Export: {e}")
    
    try:
        image_buffer = exporter.to_image(brd_markdown)
        image_size = len(image_buffer.getvalue())
        print(f"[OK] PNG Export: {image_size} bytes")
    except Exception as e:
        print(f"[FAIL] PNG Export: {e}")
    
    print()
    print("=" * 100)
    print("INTEGRATION TEST RESULT:", "PASSED [OK]" if all_valid else "FAILED [FAIL]")
    print("=" * 100)
    
    return all_valid


if __name__ == "__main__":
    success = test_integration()
    sys.exit(0 if success else 1)
