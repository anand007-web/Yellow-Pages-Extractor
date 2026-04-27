from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import time

def extract_one_item_html():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        Stealth().apply_stealth_sync(page)
        page.goto("https://yellowpages.com.eg/en/search/ice_cream-manufacturer/p1", wait_until="domcontentloaded")
        time.sleep(10)
        
        item_html = page.evaluate("""() => {
            const item = document.querySelector('.item-title');
            if (!item) return "NOT FOUND";
            const container = item.closest('.row') || item.parentElement.parentElement.parentElement;
            return container ? container.outerHTML : "CONTAINER NOT FOUND";
        }""")
        
        print("HTML of one item:")
        print(item_html[:2000]) # Print first 2000 chars
        browser.close()

if __name__ == "__main__":
    extract_one_item_html()
