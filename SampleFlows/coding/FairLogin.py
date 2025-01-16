from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the login page
        page.goto("https://identitysso.betfair.com/view/login")

        # Fill in the email/username input field
        page.fill('input[type="email"]', 'your_email@example.com')

        # Fill in the password input field
        page.fill('input[type="password"]', 'your_password')

        # Check the remember me checkbox (if present)
        page.check('input[type="checkbox"]', name='rememberMe')

        # Click the login button
        page.click('button:has-text("Login")')

        # Optionally, add a wait for navigation to ensure the login is successful
        page.wait_for_url("https://www.betfair.com/")

        # Close the browser
        browser.close()

if __name__ == "__main__":
    main()