import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_apple() -> dict:
    url = "https://jobs.apple.com/en-us/search?team=Internships"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    if "intern" not in text.lower():
        return None
    title = "Apple Internship"
    for heading in soup.find_all(["h1", "h2", "h3"]):
        if "intern" in heading.get_text(strip=True).lower():
            title = heading.get_text(strip=True)
            break
    location = "Cupertino, CA (Multiple)"
    deadline = None
    apply_url = "https://jobs.apple.com/en-us/search?team=Internships"
    return {
        "id": "apple-intern-" + str(datetime.now().year + 1),
        "title": title,
        "company": "Apple",
        "type": "internship",
        "category": "top-tier",
        "url": apply_url,
        "location": location,
        "work_type": "hybrid",
        "date_scraped": datetime.now().isoformat()[:10],
    }
