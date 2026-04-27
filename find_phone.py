import time
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

def find_phone_selector():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        Stealth().apply_stealth_sync(page)
        
        url = "https://yellowpages.com.eg/en/search/ice_cream-manufacturer/p1"
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(5)
        
        # Search for buttons
        elements = page.evaluate("""() => {
            const results = [];
            const buttons = document.querySelectorAll('button, a.btn, .phone-div, .call-us');
            buttons.forEach(el => {
                results.push({tag: el.tagName, class: el.className, text: el.innerText.trim()});
            });
            return results;
        }""")
        
        print("Found elements:")
        for res in elements:
            print(res)
            
        browser.close()

if __name__ == "__main__":
    find_phone_selector()
