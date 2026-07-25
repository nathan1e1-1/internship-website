import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_meta() -> dict:
    url = "https://www.metacareers.com/jobs/?roles[0]=Internship"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    keywords = ["university", "meta"]
    if not any(kw in text.lower() for kw in keywords):
        return None
    title = "Meta University"
    for heading in soup.find_all(["h1", "h2", "h3"]):
        if any(kw in heading.get_text(strip=True).lower() for kw in keywords):
            title = heading.get_text(strip=True)
            break
    location = "Menlo Park, CA (Multiple)"
    deadline = None
    apply_url = "https://www.metacareers.com/jobs/?roles[0]=Internship"
    return {
        "id": "meta-university-" + str(datetime.now().year + 1),
        "title": title,
        "company": "Meta",
        "type": "internship",
        "category": "top-tier",
        "url": apply_url,
        "location": location,
        "work_type": "hybrid",
        "date_scraped": datetime.now().isoformat()[:10],
    }
