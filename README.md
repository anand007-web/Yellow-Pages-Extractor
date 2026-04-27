# Egypt Yellow Pages Scraper

A robust Python-based web scraper designed to extract business information from the Egypt Yellow Pages directory.

## Description

This tool automates the extraction of business listings (Names, Addresses, and Phone Numbers) from [yellowpages.com.eg](https://yellowpages.com.eg). It is built using Playwright and incorporates stealth measures to minimize detection by anti-bot systems like Cloudflare.

### Key Features
- **Dynamic Phone Number Extraction**: Automatically fetches hidden phone numbers by interacting with the site's internal API.
- **Stealth Integration**: Uses `playwright-stealth` to mask automated browser fingerprints.
- **Pagination Support**: Automatically calculates the total number of pages and iterates through them.
- **Persistent Context**: Saves browser data to a local directory to maintain session state and reduce the frequency of captchas.
- **Manual Captcha Handling**: Automatically pauses and alerts the user when a captcha or "Attention Required" page is detected.

## Requirements

To run this scraper, you need the following installed on your system:

### 1. Python
- Python 3.7 or higher

### 2. Python Packages
- `playwright`: The core browser automation library.
- `playwright-stealth`: Plugin to prevent bot detection.

### 3. Browser Binaries
- Chromium (installed via Playwright)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/yellowpages-egypt-scraper.git
   cd yellowpages-egypt-scraper
   ```

2. Install the required Python packages:
   ```bash
   pip install playwright playwright-stealth
   ```

3. Install the Playwright browser binaries:
   ```bash
   playwright install chromium
   ```

## Usage

Run the main scraper script:

```bash
python scraper.py
```

### How it works:
1. The script launches a Chromium browser in non-headless mode (so you can see the progress and solve captchas if they appear).
2. It navigates to the search results page.
3. If a captcha is detected, the console will prompt you to solve it manually. Press **Enter** in the terminal once you've solved it.
4. The script will scrape business data page by page.
5. Results are saved in `results.txt` in the format `Name:Address:Phone`.

## Disclaimer
This tool is for educational purposes only. Please respect the terms of service of the website and use it responsibly. Excessive scraping may lead to IP blocks.
