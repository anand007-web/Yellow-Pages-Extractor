from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import time

def list_classes():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        Stealth().apply_stealth_sync(page)
        page.goto("https://yellowpages.com.eg/en/search/ice_cream-manufacturer/p1", wait_until="domcontentloaded")
        time.sleep(10)
        
        classes = page.evaluate("""() => {
            return Array.from(new Set(Array.from(document.querySelectorAll('*')).map(el => el.className))).filter(c => typeof c === 'string' && c.length > 0);
        }""")
        
        print("Classes found on page:")
        for c in sorted(classes):
            if 'phone' in c.lower() or 'call' in c.lower() or 'tel' in c.lower() or 'item' in c.lower():
                print(c)
        browser.close()

if __name__ == "__main__":
    list_classes()
