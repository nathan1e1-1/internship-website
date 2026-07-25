import requests
import os
from datetime import datetime

def _normalize(entry: dict) -> dict:
    company = entry.get("company", "Unknown")
    title = entry.get("title", "Unknown")
    year = str(datetime.now().year)
    entry_id = f"{company.lower().replace(' ', '-')}-{title.lower().replace(' ', '-')}-{year}"
    return {
        "id": entry_id,
        "title": title,
        "company": company,
        "type": "internship",
        "category": "general",
        "url": entry.get("url", ""),
        "location": entry.get("location", "TBD"),
        "work_type": entry.get("work_type", "in-person"),
        "eligibility": entry.get("eligibility"),
        "date_posted": entry.get("date_posted"),
        "deadline": entry.get("deadline"),
        "notes": entry.get("notes"),
        "date_scraped": datetime.now().isoformat()[:10],
    }

def scrape_simplify(url: str, api_key: str = None) -> list:
    headers = {}
    key = api_key or os.environ.get("SIMPLIFY_API_KEY")
    if key:
        headers["Authorization"] = f"Bearer {key}"
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("data", []) if isinstance(data, dict) else data
    if not isinstance(items, list):
        return []
    return [_normalize(item) for item in items if isinstance(item, dict)]
