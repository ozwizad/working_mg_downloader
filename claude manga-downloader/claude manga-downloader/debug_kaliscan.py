import cloudscraper
import requests

url = "https://kaliscan.com/manga/martial-wild-west/chapter-100" # Guessing URL structure based on user input
print(f"Testing Kaliscan: {url}")

scraper = cloudscraper.create_scraper()
try:
    resp = scraper.get(url, timeout=10)
    print(f"Page Status: {resp.status_code}")
    
    if resp.status_code != 200:
        print("Failed to fetch page.")
        
    # If 403, it definitely needs DrissionPage
except Exception as e:
    print(f"Page Error: {e}")

# Test direct image access if possible (mocking a known image path structure if I could guess it, but I can't)
# So I'll just rely on page access status. 
# Kaliscan usually has Cloudflare.
