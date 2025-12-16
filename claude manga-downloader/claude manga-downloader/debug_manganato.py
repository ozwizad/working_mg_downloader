import cloudscraper
from bs4 import BeautifulSoup

url = "https://www.manganato.gg/manga/gray-ash-the-dismissed-knight-begins-anew-in-the-dungeon-city"
scraper = cloudscraper.create_scraper()
print(f"Fetching {url}...")
try:
    resp = scraper.get(url)
    print(f"Status: {resp.status_code}")
    soup = BeautifulSoup(resp.content, 'html.parser')
    
    # Check title
    title = soup.find('h1')
    print(f"Title: {title.text.strip() if title else 'Not Found'}")
    
    # Try finding chapter list
    print("\nSearching for chapters...")
    
    # Attempt 1: Standard Manganato
    ul = soup.find('ul', class_='row-content-chapter')
    if ul:
        print("Found ul.row-content-chapter")
        print(f"Items: {len(ul.find_all('li'))}")
    else:
        print("NOT FOUND: ul.row-content-chapter")
        
    # Attempt 2: Look for any list with 'chapter' links
    print("\nLooking for any links with 'chapter' in them...")
    links = soup.find_all('a', href=True)
    count = 0
    for link in links:
        if 'chapter' in link.get('href', '') and count < 5:
            print(f"Link: {link.text.strip()} -> {link.get('href')}")
            print(f"Parent classes: {link.parent.get('class')}")
            print(f"Container classes: {link.parent.parent.get('class')}")
            count += 1
            
    # Save HTML for inspection
    with open('debug_html.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    print("Saved HTML to debug_html.html")
    
    # Inspect div.chapter-list
    print("\nInspecting div.chapter-list structure:")
    div_list = soup.find('div', class_='chapter-list')
    if div_list:
        # Check for ul
        ul = div_list.find('ul')
        if ul:
             print("Found UL inside div.chapter-list")
             lis = ul.find_all('li')
             print(f"Found {len(lis)} LI items")
             if lis:
                 print(f"Sample LI HTML: {lis[0]}")
        else:
             print("No UL found inside. Checking direct clean links...")
             links = div_list.find_all('a', href=True)
             print(f"Found {len(links)} links directly or nested.")
             if links:
                 print(f"First link: {links[0].text} -> {links[0].get('href')}")
    
except Exception as e:
    print(f"Error: {e}")
