from DrissionPage import ChromiumPage, ChromiumOptions
import time
import os

def find_browser_path():
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    for path in paths:
        if os.path.exists(path):
            return path
    return None

url = "https://mangafire.to/manga/martial-wild-westt.92po0"
print(f"Testing Mangafire: {url}")

browser_path = find_browser_path()
co = ChromiumOptions()
co.set_paths(browser_path=browser_path)
co.headless(False)
page = ChromiumPage(co)

try:
    page.get(url)
    time.sleep(5)
    
    print(f"Title: {page.title}")
    
    # Try to find chapters
    # Mangafire usually has a chapter list. Let's look for common selectors or just dump links
    links = page.eles('tag:a')
    chapter_links = []
    for link in links:
        href = link.attr('href')
        text = link.text
        if href and ('chapter' in href or 'read' in href) and len(text) < 50:
             chapter_links.append((text, href))
             
    print(f"Potential Chapters Found: {len(chapter_links)}")
    for txt, href in chapter_links[:5]:
        print(f" - {txt}: {href}")

    # If this works, I can trust scrape_protected to find images if I add logic for it.
except Exception as e:
    print(f"Error: {e}")
finally:
    page.quit()
