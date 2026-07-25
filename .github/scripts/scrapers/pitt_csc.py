import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def _extract_text(cell) -> str:
    """Extract clean text from a table cell."""
    text = cell.get_text(strip=True)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text

def _extract_apply_url(cell) -> str:
    """Extract the application URL from the cell containing apply buttons."""
    # Find all links in the cell
    links = cell.find_all('a', href=True)
    for link in links:
        href = link.get('href', '')
        # Skip simplify.jobs links, get the actual application URL
        if 'simplify.jobs' not in href and href.startswith('http'):
            return href
    # Fallback: return first http link
    for link in links:
        href = link.get('href', '')
        if href.startswith('http'):
            return href
    return ''

def _parse_age(age_text: str) -> str:
    """Convert age text like '1d', '4d', '2w' to approximate date_posted."""
    if not age_text:
        return None
    age_text = age_text.strip().lower()
    today = datetime.now()
    try:
        if age_text.endswith('d'):
            days = int(age_text[:-1])
            date = today - timedelta(days=days)
            return date.strftime('%Y-%m-%d')
        elif age_text.endswith('w'):
            weeks = int(age_text[:-1])
            date = today - timedelta(weeks=weeks)
            return date.strftime('%Y-%m-%d')
        elif age_text.endswith('m'):
            months = int(age_text[:-1])
            date = today - timedelta(days=months * 30)
            return date.strftime('%Y-%m-%d')
    except (ValueError, IndexError):
        pass
    return None

def _normalize_entry(company: str, title: str, location: str, url: str, age_text: str) -> dict:
    year = str(datetime.now().year)
    # Create a clean ID
    clean_company = re.sub(r'[^a-z0-9]', '-', company.lower())[:20].strip('-')
    clean_title = re.sub(r'[^a-z0-9]', '-', title.lower())[:30].strip('-')
    entry_id = f"{clean_company}-{clean_title}-{year}"
    
    return {
        "id": entry_id,
        "title": title,
        "company": company,
        "type": "internship",
        "category": "general",
        "url": url,
        "location": location if location else "TBD",
        "work_type": "in-person",
        "date_posted": _parse_age(age_text),
        "date_scraped": datetime.now().isoformat()[:10],
    }

def scrape_pitt_csc(url: str) -> list:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    
    entries = []
    tables = soup.find_all('table')
    
    for table in tables:
        tbody = table.find('tbody')
        if not tbody:
            continue
        rows = tbody.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 5:
                continue
            
            company = _extract_text(cells[0])
            title = _extract_text(cells[1])
            location = _extract_text(cells[2])
            url = _extract_apply_url(cells[3])
            age_text = _extract_text(cells[4])
            
            if not company or not title:
                continue
            
            entry = _normalize_entry(company, title, location, url, age_text)
            if entry["url"]:
                entries.append(entry)
    
    return entries
