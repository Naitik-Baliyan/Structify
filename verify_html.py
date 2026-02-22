"""Quick verification of HTML structure"""
import os

html_file = r"c:\Users\ASUS\Desktop\Structify\Frontend\chat.html"

if os.path.exists(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key elements
    elements = [
        ('chat-wrapper', 'Main container'),
        ('userInput', 'Input field'),
        ('sendBtn', 'Send button'),
        ('chatMessages', 'Messages area'),
        ('brdModal', 'BRD modal'),
        ('generateBrdBtn', 'Generate button'),
    ]
    
    print("\n=== HTML STRUCTURE CHECK ===\n")
    all_found = True
    for elem, desc in elements:
        if f'id="{elem}"' in content or f'class="{elem}"' in content:
            print(f'✅ {desc} ({elem})')
        else:
            print(f'❌ {desc} ({elem})')
            all_found = False
    
    # Check scripts
    print("\n=== SCRIPT REFERENCES ===\n")
    scripts = ['config.js', 'auth.js', 'chat.js', 'style.css']
    for script in scripts:
        if script in content:
            print(f'✅ {script}')
        else:
            print(f'❌ {script}')
    
    if all_found:
        print("\n✅ All required HTML elements present!\n")
    else:
        print("\n⚠️  Some elements missing - check HTML structure\n")
else:
    print(f"❌ HTML file not found: {html_file}")
