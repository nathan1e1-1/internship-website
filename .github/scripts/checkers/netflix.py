import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_netflix() -> dict:
    url = "https://jobs.netflix.com/jobs"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    if "intern" not in text.lower():
        return None
    return {
        "id": "netflix-intern-" + str(datetime.now().year + 1),
        "title": "Netflix Software Engineer Intern",
        "company": "Netflix",
        "type": "internship",
        "category": "top-tier",
        "url": url,
        "location": "Los Gatos, CA (Multiple)",
        "work_type": "hybrid",
        "season": f"Summer {datetime.now().year + 1}",
        "date_scraped": datetime.now().isoformat()[:10],
    }
