from playwright.sync_api import sync_playwright
import time
import os

OUTPUT_DIR = os.path.join(os.getcwd(), 'tests')
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    # Pre-populate localStorage so auth redirect does not occur
    context.add_init_script("window.localStorage.setItem('structify_current_user', JSON.stringify({id:1,name:'E2E Tester',email:'e2e@local.test'}));")
    page = context.new_page()

    analyze_responses = []

    def on_response(response):
        try:
            url = response.url
            if '/analyze' in url:
                try:
                    body = response.text()
                except Exception:
                    body = '<unreadable body>'
                analyze_responses.append({'url': url, 'status': response.status, 'body': body})
        except Exception as e:
            print('Response handler error:', e)

    page.on('response', on_response)

    print('Opening chat page...')
    page.goto('http://127.0.0.1:8080/chat.html')

    textarea = '#userInput'
    page.wait_for_selector(textarea, timeout=10000)

    # Send idea
    page.fill(textarea, 'A task app')
    page.keyboard.press('Enter')
    time.sleep(0.6)

    # Send target market
    page.fill(textarea, 'Small teams')
    page.keyboard.press('Enter')
    time.sleep(0.6)

    # Send problem statement
    page.fill(textarea, 'Lack of simple collaboration')
    page.keyboard.press('Enter')

    # Wait for backend analyze response
    time.sleep(2)

    screenshot_path = os.path.join(OUTPUT_DIR, 'e2e_chat.png')
    page.screenshot(path=screenshot_path, full_page=True)
    print('Saved screenshot:', screenshot_path)

    if analyze_responses:
        for r in analyze_responses:
            print('--- /analyze response ---')
            print('URL:', r['url'])
            print('Status:', r['status'])
            print('Body:', r['body'])
    else:
        print('No /analyze responses captured')

    browser.close()
