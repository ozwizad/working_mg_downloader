import requests
import time

URL = "http://localhost:5000/api/download"

payload = {
    "title": "Parallel Test",
    "chapters": [
        # Using a reliable manga URL (One Piece or similar popular one usually stays up)
        # Using Manganato (Static/Fast)
        {"url": "https://chapmanganato.to/manga-dn980422/chapter-1", "title": "Ch1"},
        {"url": "https://chapmanganato.to/manga-dn980422/chapter-2", "title": "Ch2"}
    ]
}

print("Sending parallel download request...")
start = time.time()
try:
    response = requests.post(URL, json=payload, stream=True)
    if response.status_code == 200:
        print(f"Success! Time taken: {time.time() - start:.2f}s")
        # Consume content to finish
        for chunk in response.iter_content(chunk_size=8192):
            pass
        print("Download finished.")
    else:
        print(f"Failed: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Error: {e}")
