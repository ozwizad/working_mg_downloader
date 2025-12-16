from app import scraper_instance

# Test URL
url = "https://www.manganato.gg/manga/gray-ash-the-dismissed-knight-begins-anew-in-the-dungeon-city/chapter-5"

print(f"Testing Scraper logic for: {url}")
try:
    response = scraper_instance.scraper.get(url)
    with open('debug_html.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Dumped HTML to debug_html.html")
    # Test Site Detection
    site_type = scraper_instance.detect_site(url)
    print(f"Detected Site Type: {site_type}")

    # Test Image Extraction
    print(f"Attempting to extract images from: {url}")
    images = scraper_instance.get_chapter_images(url, site_type)
    print(f"Images Found: {len(images)}")
    for i, img in enumerate(images[:5]):
        print(f" - Image {i+1}: {img}")
    
    if images:
        print("\nAttempting to download first image...")
        img_url = images[0]
        # Try with strict referer
        headers = {
            'Referer': url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        scraper_instance.scraper.headers.update(headers)
        
        resp = scraper_instance.scraper.get(img_url)
        print(f"Download Status: {resp.status_code}")
        print(f"Content Length: {len(resp.content)}")
        
        # Save error content to check what it is
        with open('image_error.html', 'wb') as f:
            f.write(resp.content)
        print("Saved response content to image_error.html")
    
except Exception as e:
    print(f"Error: {e}")
