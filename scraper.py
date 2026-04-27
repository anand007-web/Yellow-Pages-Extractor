import time
import random
import re
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

def scrape_yellowpages():
    user_data_dir = "./browser_data"
    
    with sync_playwright() as p:
        print("Launching browser...")
        # Using headless=False so the user can solve captchas
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720}
        )
        
        page = browser_context.pages[0]
        Stealth().apply_stealth_sync(page)
        
        base_url = "https://yellowpages.com.eg/en/search/bakery-product-manufacturer/p"
        all_results = []
        page_num = 1
        max_pages = 1
        
        while page_num <= max_pages:
            url = f"{base_url}{page_num}"
            print(f"\n--- Scraping Page {page_num} of {max_pages if max_pages > 1 else '?'} ---")
            
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                time.sleep(5) # Wait for Cloudflare/Loading
                
                # Manual solve check
                if "Attention Required" in page.title() or "Verify you are human" in page.content():
                    print("!! Blocked by Cloudflare !! Please solve the captcha in the browser.")
                    input("Press Enter here after you have solved the captcha and the results are visible...")
                
                # Wait for listings
                page.wait_for_selector('.item-title', timeout=20000)
                
                # Update max_pages
                if page_num == 1:
                    showing_text = page.inner_text('.showing-numbers') if page.query_selector('.showing-numbers') else ""
                    match = re.search(r'of\s+([\d,]+)', showing_text)
                    if match:
                        total = int(match.group(1).replace(',', ''))
                        max_pages = (total // 21) + (1 if total % 21 > 0 else 0)
                        print(f"Detected {total} results across {max_pages} pages.")

                # Scroll to load everything
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(2)

                # Extract listings and their phone numbers
                # We will try to click each 'Show Number' or 'Call' button if needed,
                # but let's first try to find the wishId and fetch the phone endpoint 
                # or find it in the data attributes.
                
                print("Extracting data from page...")
                listings_data = page.evaluate("""async () => {
                    const results = [];
                    const items = document.querySelectorAll('.item-title');
                    
                    for (const item of items) {
                        const name = item.innerText.trim();
                        const container = item.closest('.row') || item.parentElement.parentElement.parentElement;
                        const addressTag = container ? container.querySelector('.address-text') : null;
                        const address = addressTag ? addressTag.innerText.trim() : "N/A";
                        
                        // Find wishId for phone number fetching
                        const wishIdBtn = container ? container.querySelector('[data-wishId]') : null;
                        const wishId = wishIdBtn ? wishIdBtn.getAttribute('data-wishId') : null;
                        
                        let phone = "N/A";
                        
                        if (wishId) {
                            try {
                                // Try to fetch the phone number from the endpoint
                                const response = await fetch(`/en/getPhones/${wishId}/false`);
                                const text = await response.text();
                                // The response is often an HTML fragment with the phone number
                                const tempDiv = document.createElement('div');
                                tempDiv.innerHTML = text;
                                phone = tempDiv.innerText.trim().replace(/\\s+/g, ', ');
                            } catch (e) {
                                phone = "Error fetching phone";
                            }
                        }
                        
                        results.push(`${name}:${address}:${phone}`);
                    }
                    return results;
                }""")
                
                if listings_data:
                    new_items = 0
                    for entry in listings_data:
                        if entry not in all_results:
                            all_results.append(entry)
                            new_items += 1
                    print(f"Added {new_items} items. Total: {len(all_results)}")
                
                # Next page
                if page_num < max_pages:
                    next_page_exists = page.query_selector(f"a[href*='/p{page_num + 1}']")
                    if next_page_exists:
                        page_num += 1
                        time.sleep(random.uniform(5, 10))
                    else:
                        print("Next page link not found. Stopping.")
                        break
                else:
                    break
                    
            except Exception as e:
                print(f"Error on page {page_num}: {e}")
                break
                
        # Save results
        with open("results.txt", "w", encoding="utf-8") as f:
            for item in all_results:
                f.write(item + "\n")
        
        print(f"\nFinished! Total items: {len(all_results)}")
        print("Results saved to results.txt")
        browser_context.close()

if __name__ == "__main__":
    scrape_yellowpages()
