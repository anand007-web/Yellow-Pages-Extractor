from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        Stealth().apply_stealth_sync(page)
        print("Stealth applied successfully!")
        browser.close()

if __name__ == "__main__":
    test()
