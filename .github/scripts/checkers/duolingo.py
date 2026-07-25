import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_duolingo() -> dict:
    url = "https://careers.duolingo.com/"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    keywords = ["thrive", "intern"]
    if not any(kw in text.lower() for kw in keywords):
        return None
    title = "Duolingo Thrive / Internship"
    for heading in soup.find_all(["h1", "h2", "h3"]):
        if any(kw in heading.get_text(strip=True).lower() for kw in keywords):
            title = heading.get_text(strip=True)
            break
    location = "Pittsburgh, PA (Remote options)"
    deadline = None
    apply_url = "https://careers.duolingo.com/"
    return {
        "id": "duolingo-thrive-" + str(datetime.now().year + 1),
        "title": title,
        "company": "Duolingo",
        "type": "internship",
        "category": "top-tier",
        "url": apply_url,
        "location": location,
        "work_type": "hybrid",
        "date_scraped": datetime.now().isoformat()[:10],
    }
