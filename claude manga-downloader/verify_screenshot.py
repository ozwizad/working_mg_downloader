import requests
import time

url = "http://127.0.0.1:5000/api/screenshot-pdf"
payload = {
    "url": "https://www.manganato.gg/manga/ice-lord/chapter-53",
    "wait_time": 10
}

print(f"Sending request to {url}...")
print(f"Payload: {payload}")

try:
    response = requests.post(url, json=payload, timeout=120)
    
    if response.status_code == 200:
        print("SUCCESS! PDF generated.")
        filename = "test_output.pdf"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"PDF saved to {filename}")
        print(f"Size: {len(response.content)} bytes")
    else:
        print(f"FAILED with status {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"ERROR: {e}")
