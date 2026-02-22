#!/usr/bin/env python3
"""
Test script for BRD Formatter implementation
Verifies the formatter generates proper Business Requirements Documents
"""

import sys
import os

# Add Backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Backend'))

from services.brd_generator import BRDFormatter

def test_brd_formatter():
    """Test BRD formatter with sample analysis data"""
    
    # Sample analysis data from AI engine
    analysis_data = {
        'idea': 'AI-Powered Customer Service Platform',
        'target_market': 'Enterprise SaaS and Customer Support Organizations',
        'problem_statement': 'Enterprises struggled with high customer support costs and slow response times',
        'analysis': 'The platform addresses a real market need with strong product-market fit potential',
        'compatibility_score': 78,
        'improvement_suggestions': [
            'Develop comprehensive go-to-market strategy',
            'Build strategic partnerships with integrations providers',
            'Establish customer success program',
            'Create detailed product roadmap'
        ],
        'risk_level': 'medium',
        'domain_tags': ['SaaS', 'Enterprise', 'Customer Service', 'AI/ML']
    }
    
    print("=" * 80)
    print("TESTING BRD FORMATTER")
    print("=" * 80)
    print()
    
    # Initialize formatter
    formatter = BRDFormatter(analysis_data)
    
    # Generate formatted BRD
    brd_content = formatter.generate_formatted_brd()
    
    print(brd_content)
    print()
    print("=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)
    
    # Verify all required sections are present
    required_sections = [
        "BUSINESS REQUIREMENTS DOCUMENT",
        "Project Name:",
        "Project Manager:",
        "Date Submitted:",
        "Document Status:",
        "1. Executive Summary",
        "2. Project Objectives",
        "3. Project Scope",
        "IN SCOPE",
        "OUT OF SCOPE",
        "4. Business Requirements",
        "5. Key Stakeholders",
        "6. Project Constraints",
        "7. Cost-Benefit Analysis"
    ]
    
    print("\nVERIFYING REQUIRED SECTIONS:")
    print("-" * 80)
    
    all_present = True
    for section in required_sections:
        if section in brd_content:
            print(f"[OK] {section}")
        else:
            print(f"[MISSING] {section}")
            all_present = False
    
    print()
    if all_present:
        print("[SUCCESS] ALL REQUIRED SECTIONS PRESENT")
    else:
        print("[FAIL] SOME SECTIONS MISSING")
    
    # Verify table formatting
    print("\nVERIFYING TABLE FORMATTING:")
    print("-" * 80)
    
    tables = {
        "Business Requirements Table": "| Priority Level | Critical Level | Requirement Description |",
        "Stakeholders Table": "| Name | Job Role | Duties |",
        "Constraints Table": "| Constraint | Description |",
        "Cost-Benefit Table": "| Cost | Benefit |"
    }
    
    for table_name, table_header in tables.items():
        if table_header in brd_content:
            print(f"[OK] {table_name}")
        else:
            print(f"[MISSING] {table_name}")
    
    # Verify business tone and conventions
    print("\nVERIFYING BUSINESS TONE:")
    print("-" * 80)
    
    tone_checks = {
        'System shall': '"System shall" format used for requirements',
        'measurable': 'Focus on measurable outcomes',
        'business': 'Business-focused language'
    }
    
    for keyword, description in tone_checks.items():
        if keyword.lower() in brd_content.lower():
            print(f"[OK] {description}")
        else:
            print(f"[WARNING] {description} (keyword: {keyword})")
    
    return all_present


if __name__ == "__main__":
    success = test_brd_formatter()
    sys.exit(0 if success else 1)
