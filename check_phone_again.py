from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import time

def find_call_us():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        Stealth().apply_stealth_sync(page)
        page.goto("https://yellowpages.com.eg/en/search/ice_cream-manufacturer/p1", wait_until="domcontentloaded")
        time.sleep(10)
        
        # Look for call-us elements
        elements = page.evaluate("""() => {
            const results = [];
            const calls = document.querySelectorAll('.call-us, .btn-phone, .phone-div, .phone-number, a[href^="tel:"]');
            calls.forEach(el => {
                results.push({
                    tag: el.tagName, 
                    class: el.className, 
                    text: el.innerText.trim(),
                    dataPhone: el.getAttribute('data-phone'),
                    href: el.getAttribute('href')
                });
            });
            return results;
        }""")
        
        print(f"Found {len(elements)} potential phone elements.")
        for res in elements:
            print(res)
            
        browser.close()

if __name__ == "__main__":
    find_call_us()
