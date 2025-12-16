from app import MangaScraper

url = "https://www.manganato.gg/manga/gray-ash-the-dismissed-knight-begins-anew-in-the-dungeon-city"

print(f"Testing App Logic for: {url}")
scraper = MangaScraper()
site_type = scraper.detect_site(url)
print(f"Detected Site Type: {site_type}")

if site_type == 'manganato':
    print("Running scrape_manganato...")
    result = scraper.scrape_manganato(url)
    if result:
        print(f"Title: {result.get('title')}")
        chapters = result.get('chapters', [])
        print(f"Chapters Found: {len(chapters)}")
        if chapters:
            print(f"First Chapter: {chapters[0]}")
    else:
        print("Result is None")
else:
    print("Runing scrape_generic...")
    result = scraper.scrape_generic(url)
    print(result)
