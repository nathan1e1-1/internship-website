import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_microsoft() -> dict:
    url = "https://careers.microsoft.com/students/us/en/us-interns"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    if "explore" not in text.lower():
        return None
    title = "Microsoft Explore"
    for heading in soup.find_all(["h1", "h2", "h3"]):
        if "explore" in heading.get_text(strip=True).lower():
            title = heading.get_text(strip=True)
            break
    location = "Redmond, WA (Multiple)"
    deadline = None
    apply_url = "https://careers.microsoft.com/students/us/en/us-interns"
    return {
        "id": "microsoft-explore-" + str(datetime.now().year + 1),
        "title": title,
        "company": "Microsoft",
        "type": "internship",
        "category": "top-tier",
        "url": apply_url,
        "location": location,
        "work_type": "hybrid",
        "date_scraped": datetime.now().isoformat()[:10],
    }
