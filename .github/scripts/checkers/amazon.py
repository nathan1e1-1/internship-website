import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_amazon() -> dict:
    url = "https://www.amazon.jobs/content/en/teams/internships"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    keywords = ["propel", "university"]
    if not any(kw in text.lower() for kw in keywords):
        return None
    title = "Amazon Propel / University Internship"
    for heading in soup.find_all(["h1", "h2", "h3"]):
        if any(kw in heading.get_text(strip=True).lower() for kw in keywords):
            title = heading.get_text(strip=True)
            break
    location = "Seattle, WA (Multiple)"
    deadline = None
    apply_url = "https://www.amazon.jobs/content/en/teams/internships"
    return {
        "id": "amazon-propel-" + str(datetime.now().year + 1),
        "title": title,
        "company": "Amazon",
        "type": "internship",
        "category": "top-tier",
        "url": apply_url,
        "location": location,
        "work_type": "hybrid",
        "date_scraped": datetime.now().isoformat()[:10],
    }
