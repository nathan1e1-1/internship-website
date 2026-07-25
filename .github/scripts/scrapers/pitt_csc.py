import requests
import re
from datetime import datetime

def _normalize_from_table(cols: list) -> dict:
    company = cols[0].strip() if len(cols) > 0 else "Unknown"
    title = cols[1].strip() if len(cols) > 1 else "Unknown"
    location = cols[2].strip() if len(cols) > 2 else "TBD"
    date_posted = cols[3].strip() if len(cols) > 3 else None
    url_match = re.search(r'\[.*?\]\((.*?)\)', cols[4]) if len(cols) > 4 else None
    url = url_match.group(1) if url_match else ""
    year = str(datetime.now().year)
    entry_id = f"{company.lower().replace(' ', '-')}-{title.lower().replace(' ', '-')}-{year}"
    return {
        "id": entry_id,
        "title": title,
        "company": company,
        "type": "internship",
        "category": "general",
        "url": url,
        "location": location,
        "work_type": "in-person",
        "date_posted": date_posted,
        "date_scraped": datetime.now().isoformat()[:10],
    }

def scrape_pitt_csc(url: str) -> list:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    lines = resp.text.splitlines()
    entries = []
    in_table = False
    for line in lines:
        if line.startswith("| Company"):
            in_table = True
            continue
        if in_table and line.startswith("|") and "---" not in line:
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 5:
                entries.append(_normalize_from_table(cols))
    return entries
