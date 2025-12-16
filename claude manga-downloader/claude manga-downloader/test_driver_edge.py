import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

def setup_driver():
    print("Setting up EDGE driver...")
    edge_options = Options()
    edge_options.add_argument('--headless')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--window-size=1920,1080')
    edge_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    # Check for Edge binary
    possible_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    
    binary_location = None
    for path in possible_paths:
        if os.path.exists(path):
            binary_location = path
            print(f"FOUND Edge at: {binary_location}")
            break
            
    if binary_location:
         edge_options.binary_location = binary_location
    
    try:
        service = Service(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=edge_options)
    except Exception as e:
        print(f"Error creating EDGE driver: {e}")
        raise

try:
    print("Starting Edge test...")
    driver = setup_driver()
    print("Edge Driver created successfully.")
    
    url = "https://www.manganato.gg/manga/ice-lord/chapter-53"
    print(f"Navigating to {url}")
    driver.get(url)
    time.sleep(5)
    print(f"Title: {driver.title}")
    
    driver.quit()
    print("Edge Test passed!")
except Exception as e:
    print(f"\nEDGE TEST FAILED WITH ERROR: {e}")
    import traceback
    traceback.print_exc()
