from DrissionPage import ChromiumPage, ChromiumOptions
import sys

# Windows console encoding fix
sys.stdout.reconfigure(encoding='utf-8')

url = "https://demonicscans.org/title/Martial-Wild-West/chapter/100/1"
# url = "https://manhuaus.com/manga/martial-wild-west/chapter-96/"

print(f"Testing DrissionPage on {url}...")

try:
    co = ChromiumOptions()
    import os
    
    # Check common paths
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    ]
    
    found_path = None
    for p in paths:
        if os.path.exists(p):
            found_path = p
            print(f"Found browser at: {p}")
            break
            
    if found_path:
        co.set_paths(browser_path=found_path)
    else:
        print("No browser found in standard paths!")
        
    co.headless(True)
    co.set_argument('--no-sandbox')
    co.set_argument('--disable-gpu')
    
    # Create page
    page = ChromiumPage(co)
    
    # Go to URL
    page.get(url)
    
    print("Waiting for cloudflare...")
    import time
    time.sleep(5)
    
    # Check title
    print(f"Title: {page.title}")
    
    # Check HTML content
    html = page.html
    print(f"HTML Preview: {html[:200]}")
    
    # Scroll to bottom to trigger lazy loading
    print("Scrolling...")
    page.scroll.to_bottom()
    time.sleep(2)
    
    # Check images
    images = page.eles('tag:img')
    print(f"Found {len(images)} images")
    
    for i, img in enumerate(images):
        src = img.attr('src') or img.attr('data-src')
        if src:
            print(f"Image {i}: {src}")
            
    page.quit()

except Exception as e:
    print(f"Error: {e}")
