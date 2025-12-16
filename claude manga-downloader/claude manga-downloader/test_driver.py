import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def setup_driver():
    print("Setting up driver...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    # Explicitly check for Chrome binary on Windows
    possible_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\%USERNAME%\AppData\Local\Google\Chrome\Application\chrome.exe",
        # Add simpler paths just in case
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"),
        os.path.expandvars(r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe")
    ]
    
    binary_location = None
    for path in possible_paths:
        expanded_path = os.path.expandvars(path)
        print(f"Checking path: {expanded_path}")
        if os.path.exists(expanded_path):
            binary_location = expanded_path
            print(f"FOUND at: {binary_location}")
            break
        else:
            print("Not found")
            
    if binary_location:
        chrome_options.binary_location = binary_location
    else:
        print("WARNING: Could not find Chrome binary in standard locations.")
    
    try:
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Error creating driver: {e}")
        raise

try:
    print("Starting test...")
    driver = setup_driver()
    print("Driver created successfully.")
    
    url = "https://www.manganato.gg/manga/ice-lord/chapter-53"
    print(f"Navigating to {url}")
    driver.get(url)
    time.sleep(5)
    print(f"Title: {driver.title}")
    
    driver.quit()
    print("Test passed!")
except Exception as e:
    print(f"\nTEST FAILED WITH ERROR: {e}")
    import traceback
    traceback.print_exc()
