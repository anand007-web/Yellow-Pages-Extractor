import requests
from bs4 import BeautifulSoup

def test_scrape():
    url = "https://yellowpages.com.eg/en/search/ice_cream-manufacturer/p1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    print(f"Testing page 1...")
    response = requests.get(url, headers=headers, timeout=15)
    print(f"Status: {response.status_code}")
    print(f"Content Length: {len(response.text)}")
    print(f"Content Preview: {response.text[:500]}")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    titles = soup.find_all('a', class_='item-title')
    print(f"Found {len(titles)} titles.")
    
    for title_tag in titles:
        name = title_tag.get_text(strip=True)
        # In Yellowpages, the structure is often:
        # <div class="item-info">
        #   <a class="item-title">...</a>
        #   ...
        #   <div class="address-div">
        #     <a class="address-text">...</a>
        #   </div>
        # </div>
        
        # Let's try to find the common ancestor
        item_container = title_tag.find_parent('div', class_='row') # Usually each listing is a row
        if not item_container:
            item_container = title_tag.find_parent('div')
            
        address_tag = item_container.find('a', class_='address-text') if item_container else None
        
        if not address_tag:
            # Fallback to searching nearby
            address_tag = title_tag.find_next('a', class_='address-text')
            
        address = address_tag.get_text(strip=True) if address_tag else "N/A"
        print(f"{name}:{address}")

if __name__ == "__main__":
    test_scrape()
