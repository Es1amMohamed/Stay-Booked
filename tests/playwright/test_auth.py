from playwright.sync_api import sync_playwright

def test_signup():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/accounts/register")

        page.fill("input[name='user_name']", "testuser")
        page.fill("input[name='email']", "testmail145104@gmail.com")
        page.fill("input[name='phone_number']", "011223300")
        page.fill("input[name='password1']", "StrongPass123")
        page.fill("input[name='password2']", "StrongPass123")
        page.click("button[type='submit']")
