import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_salesforce() -> dict:
    url = "https://careers.salesforce.com"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    if "futureforce" not in text.lower() and "intern" not in text.lower():
        return None
    return {
        "id": "salesforce-intern-" + str(datetime.now().year + 1),
        "title": "Salesforce Futureforce Intern",
        "company": "Salesforce",
        "type": "internship",
        "category": "top-tier",
        "url": url,
        "location": "San Francisco, CA (Multiple)",
        "work_type": "hybrid",
        "season": f"Summer {datetime.now().year + 1}",
        "date_scraped": datetime.now().isoformat()[:10],
    }
