from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import cloudscraper
from bs4 import BeautifulSoup
import json
import re
from PIL import Image
from io import BytesIO
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import time
from DrissionPage import ChromiumPage, ChromiumOptions

app = Flask(__name__)
CORS(app)

def find_browser_path():
    import os
    paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
    ]
    for p in paths:
        if os.path.exists(p): return p
    return None

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

class MangaScraper:
    def __init__(self):
        # Cloudscraper automatically handles Cloudflare and User-Agent
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        self.headers = {
            'Referer': 'https://google.com'
        }
        self.browser_path = find_browser_path()
    
    def detect_site(self, url):
        """Detect which manga site the URL is from"""
        if 'mangadex.org' in url:
            return 'mangadex'
        elif 'manganato' in url or 'chapmanganato' in url:
            return 'manganato'
        elif 'demonicscans' in url or 'manhuaus' in url or 'asuracomic' in url or 'asura.gg' in url or 'mangafire.to' in url or 'kaliscan' in url:
            return 'protected'
        else:
            return 'generic'

    def scrape_protected(self, url):
        """Scrape protected sites using DrissionPage"""
        if not self.browser_path:
            raise Exception("Browser executable not found! Please install Chrome or Edge.")
            
        print(f"DrissionPage Scraping: {url}")
        images = []
        chapters = []
        title = "Unknown Manga"
        
        try:
            co = ChromiumOptions()
            co.set_paths(browser_path=self.browser_path)
            # Disable headless to bypass strict detection
            co.headless(False) 
            co.set_argument('--no-sandbox')
            co.set_argument('--disable-gpu')
            co.set_argument('--mute-audio')
            
            page = ChromiumPage(co)
            page.get(url)
            
            # Wait for potential cloudflare
            time.sleep(3) 
            if "Just a moment" in page.title or "Cloudflare" in page.title:
                print("Waiting for Cloudflare challenge...")
                time.sleep(5)
            
            # Scroll to trigger lazy loading (Critical for DemonicScans)
            print("Scrolling...")
            page.scroll.to_bottom()
            time.sleep(3) 

            title = page.title.replace(' - Read Manga Online', '').strip()
            

            page.quit()
        except Exception as e:
            print(f"Drission Scraping Error: {e}")
            try: page.quit()
            except: pass
            
        return {
            'site': 'protected',
            'title': title,
            'images': images,
            'chapters': chapters
        }
    
    def scrape_mangadex(self, url):
        """Scrape MangaDex"""
        try:
            manga_id = re.search(r'title/([a-f0-9-]+)', url)
            if not manga_id:
                return None
            
            manga_id = manga_id.group(1)
            api_url = f'https://api.mangadex.org/manga/{manga_id}/feed?translatedLanguage[]=en&order[chapter]=asc&limit=500'
            
            response = self.scraper.get(api_url)
            data = response.json()
            
            manga_response = self.scraper.get(f'https://api.mangadex.org/manga/{manga_id}')
            manga_data = manga_response.json()
            title = manga_data['data']['attributes']['title'].get('en', 'Unknown')
            
            chapters = []
            for item in data.get('data', []):
                attrs = item['attributes']
                chapter_num = attrs.get('chapter', 'N/A')
                chapter_title = attrs.get('title', f'Chapter {chapter_num}')
                chapter_id = item['id']
                
                chapters.append({
                    'number': chapter_num,
                    'title': chapter_title,
                    'url': f'https://mangadex.org/chapter/{chapter_id}',
                    'id': chapter_id
                })
            
            return {'title': title, 'chapters': chapters}
        except Exception as e:
            print(f"MangaDex error: {e}")
            return None
    
    def scrape_manganato(self, url):
        """Scrape Manganato"""
        try:
            print(f"Scraping Manganato: {url}")
            resp = self.scraper.get(url)
            
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            title_elem = soup.find('h1')
            title = title_elem.text.strip() if title_elem else 'Unknown'
            if title == 'Unknown':
                 title_elem = soup.select_one('.story-info-right h1')
                 if title_elem: title = title_elem.text.strip()
            
            chapters = []
            # Attempt 1: Standard Manganato (ul.row-content-chapter)
            chapter_list = soup.find('ul', class_='row-content-chapter')
            
            if chapter_list:
                for item in chapter_list.find_all('li'):
                    link = item.find('a')
                    if link:
                        chapter_url = link.get('href')
                        chapter_text = link.text.strip()
                        
                        chapter_num = re.search(r'Chapter (\d+\.?\d*)', chapter_text, re.I)
                        chapter_num = chapter_num.group(1) if chapter_num else 'N/A'
                        
                        chapters.append({
                            'number': chapter_num,
                            'title': chapter_text,
                            'url': chapter_url
                        })
            else:
                # Attempt 2: Manganato.gg Style (div.chapter-list)
                div_list = soup.find('div', class_='chapter-list')
                if div_list:
                    print("Found div.chapter-list (Manganato.gg style)")
                    links = div_list.find_all('a', href=True)
                    for link in links:
                        chapter_url = link.get('href')
                        chapter_text = link.text.strip()
                        
                        chapter_num = re.search(r'Chapter (\d+\.?\d*)', chapter_text, re.I)
                        chapter_num = chapter_num.group(1) if chapter_num else 'N/A'
                        
                        chapters.append({
                            'number': chapter_num,
                            'title': chapter_text,
                            'url': chapter_url
                        })
                        
                # Fallback: Check if it's a single chapter page
                elif 'chapter' in url:
                    # Construct a single chapter entry
                    print("No chapter list found, assuming single chapter URL")
                    chapter_num = re.search(r'chapter[-_]?(\d+\.?\d*)', url, re.I)
                    chapter_num = chapter_num.group(1) if chapter_num else '1'
                    
                    chapters.append({
                        'number': chapter_num,
                        'title': f"{title} - Chapter {chapter_num}",
                        'url': url
                    })
            
            return {'title': title, 'chapters': chapters}
        except Exception as e:
            print(f"Manganato error: {e}")
            return None

    def scrape_generic(self, url):
        """Generic scraper for unknown sites"""
        try:
            print(f"Attempting generic scrape for: {url}")
            
            response = self.scraper.get(url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find title
            title = None
            for selector in ['h1', 'h2', '.manga-title', '.title', '#manga-title', '.post-title', '#chapter-heading']:
                elem = soup.select_one(selector)
                if elem:
                    title = elem.text.strip()
                    break
            
            if not title:
                title = 'Unknown Manga'
            
            chapters = []
            
            # Look for common chapter list patterns
            chapter_containers = soup.find_all(['ul', 'div', 'li', 'select'], class_=lambda x: x and any(
                word in str(x).lower() for word in ['chapter', 'episode', 'ch-', 'list', 'select']
            ))
            
            # Strategy 1: Link-based discovery
            for container in chapter_containers:
                links = container.find_all('a', href=True)
                for link in links:
                    text = link.text.strip()
                    href = link.get('href')
                    
                    if re.search(r'(chapter|ch\.|episode|ep\.|ch-)\s*\d+', text, re.I) or re.search(r'\d+', text):
                        if not href: continue
                        if not href.startswith('http'):
                            from urllib.parse import urljoin
                            href = urljoin(url, href)
                        
                        chapter_num = 'N/A'
                        num_match = re.search(r'(\d+\.?\d*)', text)
                        if num_match:
                            chapter_num = num_match.group(1)
                        elif re.search(r'(\d+)', href):
                             num_match = re.search(r'(\d+)', href)
                             chapter_num = num_match.group(1)

                        chapters.append({
                            'number': chapter_num,
                            'title': text,
                            'url': href
                        })
            
            # Strategy 2: Option tags
            if not chapters:
                 options = soup.find_all('option', value=True)
                 for opt in options:
                    text = opt.text.strip()
                    val = opt.get('value') 
                    if 'chapter' in text.lower() or 'chapter' in val.lower() or val.startswith('http'):
                        if not val.startswith('http'): continue
                        chapters.append({
                            'number': re.search(r'\d+', text).group(0) if re.search(r'\d+', text) else 'N/A',
                            'title': text,
                            'url': val
                        })

            # Strategy 3: Elementor / Generic Title Links (Fallback)
            if not chapters:
                # Look for specific Elementor titles or any h3/h4 links that look like chapters
                potential_links = soup.select('.elementor-post__title a, h3 a, h4 a, .entry-title a')
                for link in potential_links:
                    text = link.text.strip()
                    href = link.get('href')
                    if not href: continue
                    
                    if re.search(r'(chapter|ch\.|episode|ep\.|ch-)\s*\d+', text, re.I):
                        chapters.append({
                            'number': re.search(r'\d+', text).group(0) if re.search(r'\d+', text) else '0',
                            'title': text,
                            'url': href
                        })

            # Remove duplicates
            unique_chapters = {}
            for ch in chapters:
                if 'facebook' in ch['url'] or 'twitter' in ch['url']: continue # Filter out social media links
                unique_chapters[ch['url']] = ch
            chapters = list(unique_chapters.values())
            
            # Sort
            try:
                chapters.sort(key=lambda x: float(re.search(r'[\d.]+', x['number']).group()) if re.search(r'[\d.]+', x['number']) else 0, reverse=True)
            except:
                pass
            
            return {
                'title': title,
                'chapters': chapters[:50]
            }
        except Exception as e:
            print(f"Generic scraper error: {e}")
            return None
    
    def get_chapter_images(self, chapter_url, site_type='generic'):
        """Get images from chapter"""
        try:
            print(f"Getting images for: {chapter_url} (Type: {site_type})")
            
            if site_type == 'protected':
                result = self.scrape_protected(chapter_url)
                return result.get('images', [])

            response = self.scraper.get(chapter_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            images = []
            
            if site_type == 'mangadex':
                chapter_id = re.search(r'chapter/([a-f0-9-]+)', chapter_url)
                if chapter_id:
                    api_url = f'https://api.mangadex.org/at-home/server/{chapter_id.group(1)}'
                    data = self.scraper.get(api_url).json()
                    base_url = data['baseUrl']
                    chapter_hash = data['chapter']['hash']
                    
                    for filename in data['chapter']['data']:
                        images.append(f'{base_url}/data/{chapter_hash}/{filename}')
            else:
                main_content = soup.find('div', class_=re.compile(r'reader|content|chapter-image|reading-content|container-chapter-reader|page-break'))
                target_soup = main_content if main_content else soup
                
                for img in target_soup.find_all('img'):
                    src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
                    if src and any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                        if not src.startswith('http'):
                            from urllib.parse import urljoin
                            src = urljoin(chapter_url, src)
                        
                        if any(x in src.lower() for x in ['logo', 'banner', 'button', 'icon', 'avatar', 'ads', 'disqus', 'facebook']):
                            continue
                            
                        images.append(src)
            
            return images
        except Exception as e:
            print(f"Get images error: {e}")
            return []

scraper_instance = MangaScraper()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

# --- TRACKING SYSTEM ---
TRACKING_FILE = 'tracking.json'

def load_tracking():
    if not os.path.exists(TRACKING_FILE):
        return {}
    try:
        with open(TRACKING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_tracking(data):
    with open(TRACKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/api/track/list', methods=['GET'])
def list_tracking():
    data = load_tracking()
    sorted_data = dict(sorted(data.items(), key=lambda item: item[1].get('title', '').lower()))
    return jsonify(sorted_data)

@app.route('/api/track/add', methods=['POST'])
def add_tracking():
    data = request.json
    url = data.get('url')
    if not url: return jsonify({'status': 'error', 'message': 'URL required'}), 400

    tracking_data = load_tracking()
    if url in tracking_data:
        return jsonify({'status': 'exists', 'message': 'Already tracked'})

    try:
        site_type = scraper_instance.detect_site(url)
        if site_type == 'mangadex':
            result = scraper_instance.scrape_mangadex(url)
        elif site_type == 'manganato':
            result = scraper_instance.scrape_manganato(url)
        else:
            result = scraper_instance.scrape_generic(url)
        
        if not result:
            return jsonify({'status': 'error', 'message': 'Could not scrape manga info'}), 400

        chapters = result.get('chapters', [])
        last_chapter = chapters[0]['number'] if chapters else 'N/A'
        
        tracking_data[url] = {
            'title': result['title'],
            'url': url,
            'site': site_type,
            'last_chapter': last_chapter,
            'total_chapters': len(chapters),
            'new_chapters': []
        }
        
        save_tracking(tracking_data)
        return jsonify({'status': 'success', 'data': tracking_data[url]})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/track/remove', methods=['POST'])
def remove_tracking():
    data = request.json
    url = data.get('url')
    tracking_data = load_tracking()
    if url in tracking_data:
        del tracking_data[url]
        save_tracking(tracking_data)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Not found'}), 404

@app.route('/api/track/check', methods=['POST'])
def check_updates():
    tracking_data = load_tracking()
    checked_count = 0
    for url, info in tracking_data.items():
        try:
            site_type = info['site']
            if site_type == 'mangadex':
                result = scraper_instance.scrape_mangadex(url)
            elif site_type == 'manganato':
                result = scraper_instance.scrape_manganato(url)
            else:
                result = scraper_instance.scrape_generic(url)
            
            if result and result.get('chapters'):
                current_chapters = result['chapters']
                if current_chapters:
                    latest_chap = current_chapters[0]
                    last_known_num = info.get('last_chapter', '0')
                    
                    # Check if latest chapter is different and likely newer
                    has_new = False
                    try:
                        # Try float comparison
                        import re
                        curr_num = float(re.search(r'[\d.]+', latest_chap['number']).group())
                        last_num = float(re.search(r'[\d.]+', str(last_known_num)).group())
                        if curr_num > last_num:
                            has_new = True
                    except:
                        # Fallback: simple string difference
                        if latest_chap['number'] != last_known_num:
                            has_new = True

                    if has_new:
                        # Find all chapters up to the last known one
                        new_chapters_found = []
                        for ch in current_chapters:
                            if ch['number'] == last_known_num:
                                break
                            new_chapters_found.append(ch)
                        
                        if not new_chapters_found:
                            new_chapters_found = [latest_chap]

                        info['new_chapters'] = [{'number': ch['number'], 'url': ch['url']} for ch in new_chapters_found]
                        info['last_chapter'] = latest_chap['number']
                        info['total_chapters'] = len(current_chapters)
            checked_count += 1
            time.sleep(1)
        except Exception as e:
            print(f"Update check error for {url}: {e}")
            continue
    save_tracking(tracking_data)
    return jsonify({'status': 'success', 'checked': checked_count})

@app.route('/api/scrape', methods=['POST'])
def scrape_manga():
    data = request.json
    url = data.get('url')
    if not url: return jsonify({'error': 'URL required'}), 400
    
    url = url.split('?')[0].split('#')[0]
    site_type = scraper_instance.detect_site(url)
    
    result = None
    if site_type == 'mangadex':
        result = scraper_instance.scrape_mangadex(url)
    elif site_type == 'manganato':
        result = scraper_instance.scrape_manganato(url)
    elif site_type == 'protected':
        result = scraper_instance.scrape_protected(url)
    else:
        result = scraper_instance.scrape_generic(url)
    
    if result and result.get('chapters'):
        return jsonify(result)
    else:
        return jsonify({'error': 'No chapters found. Site might be protected or layout unsupported.'}), 500

@app.route('/api/screenshot-pdf', methods=['POST'])
def screenshot_pdf():
    """Smart Screenshot: Scrapes images and creates PDF"""
    data = request.json
    url = data.get('url')
    if not url: return jsonify({'error': 'URL required'}), 400
    
    print(f"Smart Screenshot for: {url}")
    
    try:
        # 1. Scrape images
        site_type = scraper_instance.detect_site(url)
        images = scraper_instance.get_chapter_images(url, site_type)
        
        if not images:
             return jsonify({'error': 'No images found on this page'}), 404

        # 2. Create PDF with Dynamic Pages
        pdf_filename = f"screenshot_{int(time.time())}.pdf"
        pdf_path = f"/tmp/{pdf_filename}"
        if not os.path.exists('/tmp'): os.makedirs('/tmp')
        
        # Standard A4 width, but height will be variable
        pdf_width, _ = A4
        c = canvas.Canvas(pdf_path, pagesize=A4)
        
        for img_url in images[:40]: # Limit to 40 pages for speed
            try:
                # Conditional headers based on site
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                if 'manganato' in url:
                    headers['Referer'] = 'https://www.manganato.gg/'
                else:
                    headers['Referer'] = url

                img_response = scraper_instance.scraper.get(img_url, headers=headers, timeout=10)
                img = Image.open(BytesIO(img_response.content))
                if img.mode != 'RGB': img = img.convert('RGB')
                
                img_width, img_height = img.size
                if img_width == 0: continue
                
                aspect = img_height / img_width
                
                # Full width (no margins)
                new_width = pdf_width
                new_height = new_width * aspect
                
                # Set page size to exactly match image aspect
                c.setPageSize((new_width, new_height))
                
                temp_img = BytesIO()
                # Increase quality to 100 (Max)
                img.save(temp_img, format='JPEG', quality=100)
                temp_img.seek(0)
                
                # Draw at 0,0 filling the page
                c.drawImage(ImageReader(temp_img), 0, 0, width=new_width, height=new_height)
                c.showPage()
                time.sleep(0.2)
            except Exception as e:
                print(f"Image error: {e}")
                continue
                
        c.save()
        return send_file(pdf_path, as_attachment=True, download_name=pdf_filename)
        
    except Exception as e:
        print(f"Screenshot error: {e}")
        return jsonify({'error': str(e)}), 500

from concurrent.futures import ThreadPoolExecutor, as_completed

def process_chapter_data(chapter):
    """Downloads all images for a chapter into memory"""
    try:
        chapter_url = chapter.get('url')
        chapter_title = chapter.get('title', 'Unknown')
        
        site_type = scraper_instance.detect_site(chapter_url)
        images = scraper_instance.get_chapter_images(chapter_url, site_type)
        
        if not images:
            return {'title': chapter_title, 'images': []}
            
        # Download images in parallel
        print(f"Downloading {len(images)} images for {chapter_title}...")
        downloaded_images = []
        
        def download_single_image(args):
            index, img_url = args
            try:
                # Conditional headers based on site
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                if 'manganato' in chapter_url:
                    headers['Referer'] = 'https://www.manganato.gg/'
                else:
                    headers['Referer'] = chapter_url

                resp = scraper_instance.scraper.get(img_url, headers=headers, timeout=10)
                if resp.status_code == 200:
                    return index, BytesIO(resp.content)
            except Exception as e:
                pass
            return index, None

        with ThreadPoolExecutor(max_workers=10) as img_executor:
            image_tasks = list(enumerate(images))
            results = list(img_executor.map(download_single_image, image_tasks))
            
            # Sort by index and extract content
            results.sort(key=lambda x: x[0])
            downloaded_images = [r[1] for r in results if r[1] is not None]
        
        return {'title': chapter_title, 'images': downloaded_images}
    except Exception as e:
        print(f"Chapter proc error {chapter.get('title')}: {e}")
        return {'title': chapter.get('title', 'Error'), 'images': []}

@app.route('/api/download', methods=['POST'])
def download_chapters():
    data = request.json
    chapters = data.get('chapters', [])
    manga_title = data.get('title', 'manga')
    
    if not chapters: return jsonify({'error': 'No chapters selected'}), 400
    
    # Imports for zip handling
    import zipfile
    import shutil
    import time
    import tempfile # Added for tempfile.gettempdir()
    
    try:
        # Create a unique temp directory for this download
        download_id = f"dl_{int(time.time())}_{id(chapters)}"
        base_tmp_path = os.path.join(tempfile.gettempdir(), download_id)
        if not os.path.exists(base_tmp_path): os.makedirs(base_tmp_path)

        # Prepare Tasks
        tasks = []
        for i, chapter in enumerate(chapters):
            url = chapter.get('url')
            site_type = scraper_instance.detect_site(url)
            is_fast = site_type != 'protected'
            tasks.append({
                'index': i,
                'chapter': chapter,
                'fast': is_fast
            })
            
        # Results container
        chapter_results = {}
        
        # 1. Process Fast Chapters (Parallel)
        fast_tasks = [t for t in tasks if t['fast']]
        if fast_tasks:
            print(f"Processing {len(fast_tasks)} chapters in parallel (Static)...")
            with ThreadPoolExecutor(max_workers=3) as executor:
                future_to_idx = {
                    executor.submit(process_chapter_data, t['chapter']): t['index'] 
                    for t in fast_tasks
                }
                for future in as_completed(future_to_idx):
                    idx = future_to_idx[future]
                    chapter_results[idx] = future.result()
                    
        # 2. Process Slow Chapters (Sequential)
        slow_tasks = [t for t in tasks if not t['fast']]
        if slow_tasks:
            print(f"Processing {len(slow_tasks)} chapters sequentially (Protected)...")
            for t in slow_tasks:
                chapter_results[t['index']] = process_chapter_data(t['chapter'])
        
        # 3. Generate PDFs
        generated_files = []
        pdf_width, _ = A4
        
        print("Generating PDFs...")
        for i in range(len(chapters)):
            res = chapter_results.get(i)
            if not res or not res['images']: continue
            
            # Create individual PDF for this chapter
            # Sanitize filename
            safe_title = "".join([c for c in res['title'] if c.isalpha() or c.isdigit() or c in (' ', '-', '_')]).strip()
            chapter_pdf_name = f"{safe_title}.pdf"
            chapter_pdf_path = os.path.join(base_tmp_path, chapter_pdf_name)
            
            try:
                c = canvas.Canvas(chapter_pdf_path, pagesize=A4)
                
                for img_bytes in res['images']:
                    try:
                        img = Image.open(img_bytes)
                        if img.mode != 'RGB': img = img.convert('RGB')
                        
                        img_width, img_height = img.size
                        if img_width == 0: continue
                        
                        aspect = img_height / img_width
                        new_width = pdf_width
                        new_height = new_width * aspect
                        
                        c.setPageSize((new_width, new_height))
                        
                        # Save to temp bytes for ReportLab
                        temp_img = BytesIO()
                        # Increase quality to 100 (Max)
                        img.save(temp_img, format='JPEG', quality=100)
                        temp_img.seek(0)
                        
                        c.drawImage(ImageReader(temp_img), 0, 0, width=new_width, height=new_height)
                        c.showPage()
                    except Exception as e:
                        print(f"Image error: {e}")
                        continue
                
                c.save()
                generated_files.append(chapter_pdf_path)
            except Exception as e:
                print(f"PDF creation error for {chapter_pdf_name}: {e}")
                continue

        # 4. Package Response
        if not generated_files:
             return jsonify({'error': 'Failed to generate any files'}), 500

        # If single chapter, return PDF directly
        if len(chapters) == 1:
            return send_file(generated_files[0], as_attachment=True, download_name=os.path.basename(generated_files[0]))
        
        # If multiple, ZIP them
        else:
            zip_filename = f"{manga_title.replace(' ', '_')}_Chapters.zip"
            zip_path = os.path.join(tempfile.gettempdir(), f"{download_id}.zip")
            
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_path in generated_files:
                    zipf.write(file_path, os.path.basename(file_path))
            
            # Cleanup individual files folder
            try:
                shutil.rmtree(base_tmp_path)
            except: pass
            
            return send_file(zip_path, as_attachment=True, download_name=zip_filename)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        # Ensure cleanup even if an error occurs before sending file
        try:
            if 'base_tmp_path' in locals() and os.path.exists(base_tmp_path):
                shutil.rmtree(base_tmp_path)
        except: pass
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) # Debug False for production safety
