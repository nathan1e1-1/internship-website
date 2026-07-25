import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_google() -> dict:
    url = "https://buildyourfuture.withgoogle.com/programs"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    if "step" not in text.lower():
        return None
    title = "STEP Internship"
    for heading in soup.find_all(["h1", "h2", "h3"]):
        if "step" in heading.get_text(strip=True).lower():
            title = heading.get_text(strip=True)
            break
    location = "Mountain View, CA (Multiple)"
    deadline = None
    apply_url = "https://buildyourfuture.withgoogle.com/programs"
    return {
        "id": "google-step-" + str(datetime.now().year + 1),
        "title": title,
        "company": "Google",
        "type": "internship",
        "category": "top-tier",
        "url": apply_url,
        "location": location,
        "work_type": "hybrid",
        "date_scraped": datetime.now().isoformat()[:10],
    }
