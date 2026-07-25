import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_intel() -> dict:
    url = "https://jobs.intel.com"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    if "student" not in text.lower() and "intern" not in text.lower():
        return None
    return {
        "id": "intel-intern-" + str(datetime.now().year + 1),
        "title": "Intel Software Engineer Intern",
        "company": "Intel",
        "type": "internship",
        "category": "top-tier",
        "url": url,
        "location": "Santa Clara, CA (Multiple)",
        "work_type": "hybrid",
        "season": f"Summer {datetime.now().year + 1}",
        "date_scraped": datetime.now().isoformat()[:10],
    }
