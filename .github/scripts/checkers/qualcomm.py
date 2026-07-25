import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_qualcomm() -> dict:
    url = "https://qualcomm.wd5.myworkdayjobs.com/en-US/External"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    if "university" not in text.lower() and "intern" not in text.lower():
        return None
    return {
        "id": "qualcomm-intern-" + str(datetime.now().year + 1),
        "title": "Qualcomm Software Engineer Intern",
        "company": "Qualcomm",
        "type": "internship",
        "category": "top-tier",
        "url": url,
        "location": "San Diego, CA (Multiple)",
        "work_type": "hybrid",
        "season": f"Summer {datetime.now().year + 1}",
        "date_scraped": datetime.now().isoformat()[:10],
    }
