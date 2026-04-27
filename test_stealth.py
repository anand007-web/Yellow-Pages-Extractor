import time
import random
import re
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth

def test_stealth():
    with sync_playwright() as p:
        print("Testing stealth mode (headless)...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        stealth(page)
        
        base_url = "https://yellowpages.com.eg/en/search/ice_cream-manufacturer/p"
        
        for page_num in [1, 2]:
            url = f"{base_url}{page_num}"
            print(f"Checking Page {page_num}...")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                time.sleep(5)
                
                title = page.title()
                print(f"Page Title: {title}")
                
                if "Attention Required" in title or "Verify you are human" in page.content():
                    print(f"Page {page_num}: BLOCKED")
                else:
                    items = page.query_selector_all('.item-title')
                    print(f"Page {page_num}: SUCCESS. Found {len(items)} items.")
                
            except Exception as e:
                print(f"Error on page {page_num}: {e}")
            
            time.sleep(random.uniform(5, 10))
            
        browser.close()

if __name__ == "__main__":
    test_stealth()
