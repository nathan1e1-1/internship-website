import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_airbnb() -> dict:
    url = "https://www.airbnb.com/careers"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    if "internship" not in text.lower() and "university" not in text.lower():
        return None
    return {
        "id": "airbnb-intern-" + str(datetime.now().year + 1),
        "title": "Airbnb Software Engineer Intern",
        "company": "Airbnb",
        "type": "internship",
        "category": "top-tier",
        "url": url,
        "location": "San Francisco, CA",
        "work_type": "hybrid",
        "season": f"Summer {datetime.now().year + 1}",
        "date_scraped": datetime.now().isoformat()[:10],
    }
