import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_mistral() -> dict:
    url = "https://mistral.ai/careers"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    if "intern" not in text.lower():
        return None
    return {
        "id": "mistral-intern-" + str(datetime.now().year + 1),
        "title": "Mistral Software Engineer Intern",
        "company": "Mistral",
        "type": "internship",
        "category": "top-tier",
        "url": url,
        "location": "Paris, France (Remote)",
        "work_type": "hybrid",
        "season": f"Summer {datetime.now().year + 1}",
        "date_scraped": datetime.now().isoformat()[:10],
    }
