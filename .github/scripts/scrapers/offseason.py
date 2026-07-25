import requests
import re
import hashlib
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Emoji to eligibility/notes mapping
_EMOJI_MAP = {
    '🛂': 'Does NOT offer sponsorship',
    '🇺🇸': 'Requires U.S. Citizenship',
    '🔒': 'Application is closed',
    '🔥': 'FAANG+ company',
    '🎓': 'Advanced degree required',
}

def _extract_emojis(text: str) -> tuple:
    """Extract emoji indicators and return (clean_text, notes_list)."""
    notes = []
    clean = text
    for emoji, note in _EMOJI_MAP.items():
        if emoji in text:
            notes.append(note)
            clean = clean.replace(emoji, '')
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean, notes

def _extract_text(cell) -> str:
    """Extract clean text from a table cell."""
    text = cell.get_text(separator=" ", strip=True)
    text = re.sub(r'\s+', ' ', text)
    return text

def _extract_apply_url(cell) -> str:
    """Extract the application URL from the cell containing apply buttons."""
    links = cell.find_all('a', href=True)
    for link in links:
        href = link.get('href', '')
        if 'simplify.jobs' not in href and href.startswith('http'):
            return href
    for link in links:
        href = link.get('href', '')
        if href.startswith('http'):
            return href
    return ''

def _parse_age(age_text: str) -> str:
    """Convert age text like '1d', '4d', '2w', '1mo' to approximate date_posted."""
    if not age_text:
        return None
    age_text = age_text.strip().lower()
    today = datetime.now()
    try:
        if age_text.endswith('mo'):
            months = int(age_text[:-2])
            date = today - timedelta(days=months * 30)
            return date.strftime('%Y-%m-%d')
        elif age_text.endswith('d'):
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

def _normalize_entry(company: str, title: str, location: str, url: str, age_text: str, season: str, notes_list: list = None) -> dict:
    year = str(datetime.now().year)
    clean_company = re.sub(r'[^a-z0-9]', '-', company.lower())[:20].strip('-')
    full_title_slug = re.sub(r'[^a-z0-9]', '-', title.lower()).strip('-')
    title_slug = full_title_slug[:20]
    title_hash = hashlib.md5(full_title_slug.encode()).hexdigest()[:6]
    season_slug = re.sub(r'[^a-z0-9]', '-', season.lower()).strip('-')
    entry_id = f"{clean_company}-{title_slug}-{title_hash}-{season_slug}-{year}"

    notes = notes_list or []
    location_lower = (location if location else "TBD").lower()
    work_type = "remote" if "remote" in location_lower else "in-person"

    return {
        "id": entry_id,
        "title": title,
        "company": company,
        "type": "internship",
        "category": "general",
        "url": url,
        "location": location if location else "TBD",
        "work_type": work_type,
        "season": season,
        "date_posted": _parse_age(age_text),
        "deadline": None,
        "eligibility": None,
        "notes": " | ".join(notes) if notes else None,
        "date_scraped": datetime.now().isoformat()[:10],
    }

def _split_terms(terms_text: str) -> list:
    """Split terms like 'Fall 2026, Winter 2027, Spring 2027' into list."""
    if not terms_text:
        return ["Off-Season"]
    terms = [t.strip() for t in terms_text.split(',')]
    terms = [t for t in terms if t]
    return terms if terms else ["Off-Season"]

def scrape_offseason(url: str) -> list:
    """Scrape off-season internships from an HTML table at the given URL.
    
    Returns a list of normalized internship dicts.
    If a row has multiple terms (e.g., 'Fall 2026, Winter 2027'),
    creates one entry per term.
    """
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
        current_company = ""
        current_company_notes = []

        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 6:  # Off-season has 6 columns: Company, Role, Location, Terms, Application, Age
                continue

            raw_company = _extract_text(cells[0])
            title = _extract_text(cells[1])
            location = _extract_text(cells[2])
            terms_text = _extract_text(cells[3])
            url = _extract_apply_url(cells[4])
            age_text = _extract_text(cells[5])

            # Handle continuation rows (↳ means same company as above)
            if raw_company.startswith('↳') or raw_company == '↳':
                company = current_company
                company_notes = current_company_notes
            else:
                company, company_notes = _extract_emojis(raw_company)
                current_company = company
                current_company_notes = company_notes

            clean_title, title_notes = _extract_emojis(title)
            all_notes = company_notes + title_notes

            if not company or not clean_title:
                continue

            # Create one entry per term
            terms = _split_terms(terms_text)
            for term in terms:
                entry = _normalize_entry(company, clean_title, location, url, age_text, term, all_notes)
                if entry["url"]:
                    entries.append(entry)

    # Deduplicate by (company, title, location, season) keeping first occurrence
    seen = {}
    deduped = []
    for entry in entries:
        key = (entry["company"], entry["title"], entry["location"], entry["season"])
        if key not in seen:
            seen[key] = True
            deduped.append(entry)

    return deduped
