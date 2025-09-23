from playwright.sync_api import sync_playwright

def test_login_and_book_room():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("http://127.0.0.1:8000/accounts/login/")

        page.fill("input[name='email']", "testmail145104@gmail.com")
        page.fill("input[name='password']", "StrongPass123")
        page.locator("button.palatin-btn:has-text('Login')").click()
        page.goto("http://127.0.0.1:8000/rooms/13/")
        page.screenshot(path="screenshot.png")
        page.wait_for_timeout(3000)
        browser.close()