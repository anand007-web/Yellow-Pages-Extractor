def scrape_with_selenium(keyword, pages=1):
    """Scrape using Selenium to bypass Cloudflare"""
    
    # Setup headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    results = []
    base_url = "https://yellowpages.com.eg"
    
    for page in range(1, pages + 1):
        # Edit: Always include /p{page} starting from p1 to p24
        url = f"{base_url}/en/search/{keyword}/p{page}"
        print(f"Fetching page {page}: {url}")
        
        try:
            driver.get(url)
            time.sleep(5)  # Wait for page load and Cloudflare challenge
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # 🔧 FIXED: Search by class name pattern, not tag name
            company_cards = soup.find_all(lambda tag: tag.get('class') and any(cls.startswith('company-result-') for cls in tag.get('class', [])))
            
            for card in company_cards:
                name_tag = card.find('a', class_='item-title')
                company_name = name_tag.get_text(strip=True) if name_tag else None
                
                address_tag = card.find('a', class_='address-text')
                address = None
                if address_tag:
                    addr_span = address_tag.find('span')
                    address = addr_span.get_text(strip=True) if addr_span else None
                
                if company_name and address:
                    result = f"{company_name}:{address}"
                    print(result)
                    results.append(result)
            
            print(f"✓ Found {len([r for r in results if r])} results on page {page}\n")
            
        except Exception as e:
            print(f"Error: {e}")
            break
    
    driver.quit()
    return results
