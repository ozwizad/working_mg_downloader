import requests

url = "http://localhost:5000/api/scrape"
payload = {
    "url": "https://www.manganato.gg/manga/gray-ash-the-dismissed-knight-begins-anew-in-the-dungeon-city"
}

print(f"Sending POST to {url}...")
try:
    resp = requests.post(url, json=payload, timeout=20)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"Title: {data.get('title')}")
        chapters = data.get('chapters', [])
        print(f"Chapters Found: {len(chapters)}")
        if chapters:
             print(f"First: {chapters[0]}")
             print(f"Last: {chapters[-1]}")
    else:
        print(f"Error: {resp.text}")
except Exception as e:
    print(f"Exception: {e}")
