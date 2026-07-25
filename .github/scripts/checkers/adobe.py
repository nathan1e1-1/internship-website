import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_adobe() -> dict:
    url = "https://careers.adobe.com"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    if "university" not in text.lower() and "intern" not in text.lower():
        return None
    return {
        "id": "adobe-intern-" + str(datetime.now().year + 1),
        "title": "Adobe Software Engineer Intern",
        "company": "Adobe",
        "type": "internship",
        "category": "top-tier",
        "url": url,
        "location": "San Jose, CA (Multiple)",
        "work_type": "hybrid",
        "season": f"Summer {datetime.now().year + 1}",
        "date_scraped": datetime.now().isoformat()[:10],
    }
