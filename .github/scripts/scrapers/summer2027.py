import requests
import re
import hashlib
from datetime import datetime

def _extract_apply_url(cell_html: str) -> str:
    """Extract first non-simplify URL from markdown cell HTML."""
    links = re.findall(r'<a href="([^"]+)"', cell_html)
    for href in links:
        if 'simplify.jobs' not in href and href.startswith('http'):
            return href
    for href in links:
        if href.startswith('http'):
            return href
    return ''

def _extract_text(cell: str) -> str:
    """Remove HTML tags and normalize whitespace."""
    text = re.sub(r'<[^>]+>', '', cell)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def _extract_emojis(text: str) -> tuple:
    """Extract emoji indicators and return (clean_text, notes_list)."""
    _EMOJI_MAP = {
        '🛂': 'Does NOT offer sponsorship',
        '🇺🇸': 'Requires U.S. Citizenship',
        '🔒': 'Application is closed',
        '🔥': 'FAANG+ company',
        '🎓': 'Advanced degree required',
    }
    notes = []
    clean = text
    for emoji, note in _EMOJI_MAP.items():
        if emoji in text:
            notes.append(note)
            clean = clean.replace(emoji, '')
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean, notes

def _parse_date(date_text: str) -> str:
    """Convert 'Jul 24' format to approximate YYYY-MM-DD."""
    if not date_text:
        return None
    date_text = date_text.strip()
    try:
        dt = datetime.strptime(f"{date_text} {datetime.now().year}", "%b %d %Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        pass
    return None

def _normalize_entry(company: str, title: str, location: str, url: str, date_text: str, notes_list: list = None) -> dict:
    year = str(datetime.now().year)
    clean_company = re.sub(r'[^a-z0-9]', '-', company.lower())[:20].strip('-')
    full_title_slug = re.sub(r'[^a-z0-9]', '-', title.lower()).strip('-')
    title_slug = full_title_slug[:20]
    title_hash = hashlib.md5(full_title_slug.encode()).hexdigest()[:6]
    entry_id = f"{clean_company}-{title_slug}-{title_hash}-{year}"

    notes = notes_list or []

    return {
        "id": entry_id,
        "title": title,
        "company": company,
        "type": "internship",
        "category": "general",
        "url": url,
        "location": location if location else "TBD",
        "work_type": "in-person",
        "season": "Summer 2027",
        "date_posted": _parse_date(date_text),
        "deadline": None,
        "eligibility": None,
        "notes": " | ".join(notes) if notes else None,
        "date_scraped": datetime.now().isoformat()[:10],
    }

def scrape_summer2027(url: str) -> list:
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    text = resp.text

    entries = []
    current_company = ""
    current_company_notes = []

    lines = text.split('\n')
    in_table = False

    for line in lines:
        line = line.strip()
        if not line.startswith('|'):
            continue
        if re.match(r'\|[\s\-:]+\|', line):
            continue
        if 'Company' in line and 'Role' in line and 'Location' in line:
            in_table = True
            continue
        if not in_table:
            continue

        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) < 5:
            continue

        raw_company = cells[0]
        title = cells[1]
        location = cells[2]
        url = _extract_apply_url(cells[3])
        date_text = cells[4]

        if raw_company.startswith('↳') or raw_company == '↳':
            company = current_company
            company_notes = current_company_notes
        else:
            company, company_notes = _extract_emojis(_extract_text(raw_company))
            current_company = company
            current_company_notes = company_notes

        clean_title, title_notes = _extract_emojis(_extract_text(title))
        all_notes = company_notes + title_notes

        if not company or not clean_title:
            continue

        entry = _normalize_entry(company, clean_title, _extract_text(location), url, _extract_text(date_text), all_notes)
        if entry["url"]:
            entries.append(entry)

    # Deduplicate by (company, title, location) keeping first occurrence
    seen = {}
    deduped = []
    for entry in entries:
        key = (entry["company"], entry["title"], entry["location"])
        if key not in seen:
            seen[key] = True
            deduped.append(entry)

    return deduped
