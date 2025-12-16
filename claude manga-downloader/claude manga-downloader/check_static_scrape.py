import requests
from bs4 import BeautifulSoup

url = "https://www.manganato.gg/manga/ice-lord/chapter-53"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    print(f"Requesting {url}...")
    r = requests.get(url, headers=headers, timeout=10)
    print(f"Status: {r.status_code}")
    
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Manganato usually puts images in a container
    container = soup.find('div', {'class': 'container-chapter-reader'})
    if container:
        imgs = container.find_all('img')
        print(f"Found {len(imgs)} images in container")
        for i, img in enumerate(imgs[:5]):
            print(f"Img {i}: {img.get('src')}")
    else:
        print("Container not found, searching all images")
        imgs = soup.find_all('img')
        print(f"Found {len(imgs)} images total")
    
    # Try downloading first 3 images to check for 403
    for i, img in enumerate(imgs[:3]):
        src = img.get('src')
        if not src: continue
        print(f"Testing download: {src}")
        try:
             # Test WITHOUT referer first
             print("1. Testing without Referer...")
             r_img = requests.get(src, headers={'User-Agent': headers['User-Agent']}, timeout=5)
             print(f"   Status: {r_img.status_code}")
             
             # Test WITH referer
             print("2. Testing with Current URL Referer...")
             r_img2 = requests.get(src, headers={'User-Agent': headers['User-Agent'], 'Referer': url}, timeout=5)
             print(f"   Status: {r_img2.status_code}")
             
             # Test WITH manganato.com referer
             print("3. Testing with manganato.com Referer...")
             r_img3 = requests.get(src, headers={'User-Agent': headers['User-Agent'], 'Referer': 'https://manganato.com/'}, timeout=5)
             print(f"   Status: {r_img3.status_code}")
             
        except Exception as e:
            print(f"   Error: {e}")


except Exception as e:
    print(f"Error: {e}")
