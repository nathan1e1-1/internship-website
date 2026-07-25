# Multi-Source Scraper Expansion — Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add Summer 2027 and Off-Season scrapers, refactor workflow runner, and add `season` field to data model — producing ~500 total listings.

**Architecture:** Two new scraper modules (markdown table + HTML table with per-term splitting), extracted orchestrator script, optional `season` field in TypeScript types. No frontend changes.

**Tech Stack:** Python 3.11, BeautifulSoup, requests, TypeScript, Next.js 16, GitHub Actions

---

## File Structure

**New files to create:**
- `.github/scripts/scrapers/summer2027.py` — Markdown table parser for Summer 2027 repo
- `.github/scripts/scrapers/offseason.py` — HTML table parser for Off-Season repo with per-term splitting
- `.github/scripts/run_scrapers.py` — Orchestrator that calls all scrapers and checkers
- `.github/scripts/tests/test_summer2027.py` — Unit test for markdown parser
- `.github/scripts/tests/test_offseason.py` — Unit test for off-season HTML parser

**Files to modify:**
- `src/lib/types.ts` — Add optional `season` field
- `.github/scripts/scrapers/pitt_csc.py` — Add `season: "Summer 2026"` to `_normalize_entry`
- `.github/scripts/merge.py` — No changes (already handles dict merge by ID)
- `.github/workflows/scrape.yml` — Replace inline Python with `run_scrapers.py` call

---

### Task 1: Add `season` field to TypeScript types

**Files:**
- Modify: `src/lib/types.ts`

- [ ] **Step 1: Add optional `season` field**

```typescript
export interface Internship {
  id: string;
  title: string;
  company: string;
  type: 'internship' | 'fellowship' | 'program';
  category: 'top-tier' | 'general';
  url: string;
  location: string;
  work_type: 'remote' | 'hybrid' | 'in-person';
  season?: string;        // NEW
  eligibility?: string;
  date_posted?: string;
  deadline?: string;
  notes?: string;
  date_scraped: string;
}
```

- [ ] **Step 2: Commit**

```bash
git add src/lib/types.ts
git commit -m "feat: add optional season field to Internship type"
```

---

### Task 2: Update pitt_csc.py to tag entries with season

**Files:**
- Modify: `.github/scripts/scrapers/pitt_csc.py`

- [ ] **Step 1: Add `season` to `_normalize_entry` return dict**

Find the return dict in `_normalize_entry` (around line 88-102) and add `"season": "Summer 2026"`:

```python
    return {
        "id": entry_id,
        "title": title,
        "company": company,
        "type": "internship",
        "category": "general",
        "url": url,
        "location": location if location else "TBD",
        "work_type": "in-person",
        "season": "Summer 2026",  # NEW
        "date_posted": _parse_age(age_text),
        "deadline": None,
        "eligibility": None,
        "notes": " | ".join(notes) if notes else None,
        "date_scraped": datetime.now().isoformat()[:10],
    }
```

- [ ] **Step 2: Run existing scraper tests to verify no regression**

```bash
PYTHONPATH=.github/scripts python3 -m pytest .github/scripts/tests/test_pitt_csc.py -v
```

Expected output:
```
3 passed
```

- [ ] **Step 3: Commit**

```bash
git add .github/scripts/scrapers/pitt_csc.py
git commit -m "feat: tag Summer 2026 scraper entries with season field"
```

---

### Task 3: Create summer2027.py markdown table scraper

**Files:**
- Create: `.github/scripts/scrapers/summer2027.py`

- [ ] **Step 1: Write the scraper**

```python
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
        # Assume current year for month-day format
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

    # Find markdown table rows
    # Pattern: | Company | Role | Location | Link | Date Posted |
    # Split by newlines and look for table rows
    lines = text.split('\n')
    in_table = False

    for line in lines:
        line = line.strip()
        if not line.startswith('|'):
            continue
        # Skip header separator lines (| --- | --- |)
        if re.match(r'\|[\s\-:]+\|', line):
            continue
        # Skip header row
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

        # Handle continuation rows (↳ means same company as above)
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
```

- [ ] **Step 2: Commit**

```bash
git add .github/scripts/scrapers/summer2027.py
git commit -m "feat: add Summer 2027 markdown table scraper"
```

---

### Task 4: Write test for summer2027.py

**Files:**
- Create: `.github/scripts/tests/test_summer2027.py`

- [ ] **Step 1: Write the test**

```python
import pytest
from scrapers.summer2027 import scrape_summer2027

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_scrape_summer2027_parses_markdown_table(monkeypatch):
    markdown = """
# Summer 2027 Internships

| Company | Role | Location | Application/Link | Date Posted |
| ------- | ---- | -------- | ---------------- | ----------- |
| Acme Corp | Software Engineer Intern | Remote | <a href="https://apply.acme.com">Apply</a> | Jul 24 |
| Beta Inc | Data Intern 🎓 | NYC | <a href="https://apply.beta.com">Apply</a> | Jul 23 |
| ↳ | ML Intern | NYC | <a href="https://apply.beta2.com">Apply</a> | Jul 22 |
"""
    def fake_get(url, **kwargs):
        return FakeResponse(markdown)
    monkeypatch.setattr("scrapers.summer2027.requests.get", fake_get)

    result = scrape_summer2027("https://example.com/summer2027.md")
    assert len(result) == 3

    # First entry
    assert result[0]["company"] == "Acme Corp"
    assert result[0]["title"] == "Software Engineer Intern"
    assert result[0]["url"] == "https://apply.acme.com"
    assert result[0]["season"] == "Summer 2027"
    assert result[0]["date_posted"] is not None

    # Second entry with emoji
    assert result[1]["company"] == "Beta Inc"
    assert result[1]["title"] == "Data Intern"
    assert result[1]["notes"] == "Advanced degree required"

    # Continuation row
    assert result[2]["company"] == "Beta Inc"
    assert result[2]["title"] == "ML Intern"
    assert result[2]["url"] == "https://apply.beta2.com"

def test_scrape_summer2027_returns_empty_for_no_table(monkeypatch):
    markdown = "# No internships here\n\nJust some text."
    def fake_get(url, **kwargs):
        return FakeResponse(markdown)
    monkeypatch.setattr("scrapers.summer2027.requests.get", fake_get)

    result = scrape_summer2027("https://example.com/empty.md")
    assert result == []
```

- [ ] **Step 2: Run the test**

```bash
PYTHONPATH=.github/scripts python3 -m pytest .github/scripts/tests/test_summer2027.py -v
```

Expected output:
```
2 passed
```

- [ ] **Step 3: Commit**

```bash
git add .github/scripts/tests/test_summer2027.py
git commit -m "test: add unit tests for Summer 2027 scraper"
```

---

### Task 5: Create offseason.py HTML table scraper with per-term splitting

**Files:**
- Create: `.github/scripts/scrapers/offseason.py`

- [ ] **Step 1: Write the scraper**

```python
import requests
import re
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup

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
            date = today - __import__('datetime').timedelta(days=months * 30)
            return date.strftime('%Y-%m-%d')
        elif age_text.endswith('d'):
            days = int(age_text[:-1])
            date = today - __import__('datetime').timedelta(days=days)
            return date.strftime('%Y-%m-%d')
        elif age_text.endswith('w'):
            weeks = int(age_text[:-1])
            date = today - __import__('datetime').timedelta(weeks=weeks)
            return date.strftime('%Y-%m-%d')
        elif age_text.endswith('m'):
            months = int(age_text[:-1])
            date = today - __import__('datetime').timedelta(days=months * 30)
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
    # Split on comma or <br> tags
    terms = re.split(r',|<br\s*/?>', terms_text)
    terms = [t.strip() for t in terms if t.strip()]
    return terms if terms else ["Off-Season"]

def scrape_offseason(url: str) -> list:
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
```

- [ ] **Step 2: Commit**

```bash
git add .github/scripts/scrapers/offseason.py
git commit -m "feat: add Off-Season scraper with per-term entry splitting"
```

---

### Task 6: Write test for offseason.py

**Files:**
- Create: `.github/scripts/tests/test_offseason.py`

- [ ] **Step 1: Write the test**

```python
import pytest
from scrapers.offseason import scrape_offseason

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_scrape_offseason_parses_html_table_with_terms(monkeypatch):
    html = """
    <html><body>
    <table>
      <thead><tr><th>Company</th><th>Role</th><th>Location</th><th>Terms</th><th>Application</th><th>Age</th></tr></thead>
      <tbody>
        <tr>
          <td><strong><a href="https://acme.com">Acme</a></strong></td>
          <td>SWE Intern</td>
          <td>Remote</td>
          <td>Fall 2026</td>
          <td><a href="https://apply.acme.com">Apply</a></td>
          <td>1d</td>
        </tr>
        <tr>
          <td><strong><a href="https://beta.com">Beta</a></strong></td>
          <td>Data Intern</td>
          <td>NYC</td>
          <td>Fall 2026, Winter 2027, Spring 2027</td>
          <td><a href="https://apply.beta.com">Apply</a></td>
          <td>2w</td>
        </tr>
        <tr>
          <td>↳</td>
          <td>ML Intern</td>
          <td>NYC</td>
          <td>Fall 2026</td>
          <td><a href="https://apply.beta2.com">Apply</a></td>
          <td>2w</td>
        </tr>
      </tbody>
    </table>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("scrapers.offseason.requests.get", fake_get)

    result = scrape_offseason("https://example.com/offseason.html")
    
    # Acme: 1 entry (Fall 2026)
    acme_entries = [e for e in result if e["company"] == "Acme"]
    assert len(acme_entries) == 1
    assert acme_entries[0]["season"] == "Fall 2026"
    assert acme_entries[0]["title"] == "SWE Intern"

    # Beta: 3 entries (one per term)
    beta_entries = [e for e in result if e["company"] == "Beta" and e["title"] == "Data Intern"]
    assert len(beta_entries) == 3
    seasons = sorted([e["season"] for e in beta_entries])
    assert seasons == ["Fall 2026", "Spring 2027", "Winter 2027"]

    # Beta continuation row: 1 entry
    beta_ml_entries = [e for e in result if e["company"] == "Beta" and e["title"] == "ML Intern"]
    assert len(beta_ml_entries) == 1
    assert beta_ml_entries[0]["season"] == "Fall 2026"

def test_scrape_offseason_returns_empty_for_no_tables(monkeypatch):
    html = "<html><body><h1>No tables</h1></body></html>"
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("scrapers.offseason.requests.get", fake_get)

    result = scrape_offseason("https://example.com/empty.html")
    assert result == []
```

- [ ] **Step 2: Run the test**

```bash
PYTHONPATH=.github/scripts python3 -m pytest .github/scripts/tests/test_offseason.py -v
```

Expected output:
```
2 passed
```

- [ ] **Step 3: Commit**

```bash
git add .github/scripts/tests/test_offseason.py
git commit -m "test: add unit tests for Off-Season scraper with per-term splitting"
```

---

### Task 7: Create run_scrapers.py orchestrator

**Files:**
- Create: `.github/scripts/run_scrapers.py`

- [ ] **Step 1: Write the orchestrator**

```python
import sys
from scrapers.pitt_csc import scrape_pitt_csc
from scrapers.summer2027 import scrape_summer2027
from scrapers.offseason import scrape_offseason
from checkers.nvidia import check_nvidia
from checkers.google import check_google
from checkers.microsoft import check_microsoft
from checkers.meta import check_meta
from checkers.apple import check_apple
from checkers.amazon import check_amazon
from checkers.pinterest import check_pinterest
from checkers.duolingo import check_duolingo
from checkers.uber import check_uber
from merge import merge_data, write_json

def main():
    bulk = []
    sources = [
        ("Summer 2026", scrape_pitt_csc, 'https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/master/README.md'),
        ("Summer 2027", scrape_summer2027, 'https://raw.githubusercontent.com/vanshb03/Summer2027-Internships/main/README.md'),
        ("Off-Season", scrape_offseason, 'https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README-Off-Season.md'),
    ]
    
    for name, scraper, url in sources:
        try:
            entries = scraper(url)
            bulk.extend(entries)
            print(f'{name}: {len(entries)} entries')
        except Exception as e:
            print(f'{name} error: {e}', file=sys.stderr)

    top_tier = []
    for checker in [check_nvidia, check_google, check_microsoft, check_meta, check_apple, check_amazon, check_pinterest, check_duolingo, check_uber]:
        try:
            result = checker()
            if result:
                top_tier.append(result)
                print(f'{checker.__name__}: found entry')
        except Exception as e:
            print(f'{checker.__name__} error: {e}', file=sys.stderr)

    merged = merge_data(bulk, top_tier)
    write_json(merged, '../../data/internships.json')
    print(f'Wrote {len(merged)} total entries to data/internships.json')

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run a dry-run locally to verify imports work**

```bash
cd .github/scripts
python -c "from run_scrapers import main; print('Import OK')"
```

Expected output:
```
Import OK
```

- [ ] **Step 3: Commit**

```bash
git add .github/scripts/run_scrapers.py
git commit -m "refactor: extract scraper orchestrator into run_scrapers.py"
```

---

### Task 8: Update GitHub Actions workflow

**Files:**
- Modify: `.github/workflows/scrape.yml`

- [ ] **Step 1: Replace inline Python with run_scrapers.py call**

Replace the entire `Run scrapers and checkers` step:

```yaml
      - name: Run scrapers and checkers
        run: |
          cd .github/scripts
          python run_scrapers.py
```

The full workflow should now look like:

```yaml
name: Scrape Internships

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r .github/scripts/requirements.txt

      - name: Run scrapers and checkers
        run: |
          cd .github/scripts
          python run_scrapers.py

      - name: Commit if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data/internships.json
          if git diff --cached --quiet; then
            echo "No changes to commit"
          else
            git commit -m "data: daily internship scrape $(date -u +%Y-%m-%d)"
            git push
          fi
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/scrape.yml
git commit -m "ci: refactor workflow to use extracted run_scrapers.py orchestrator"
```

---

### Task 9: Run full test suite

- [ ] **Step 1: Run all Python tests**

```bash
PYTHONPATH=.github/scripts python3 -m pytest .github/scripts/tests/ -v
```

Expected output:
```
test_offseason.py::test_scrape_offseason_parses_html_table_with_terms PASSED
test_offseason.py::test_scrape_offseason_returns_empty_for_no_tables PASSED
test_pitt_csc.py::test_scrape_pitt_csc_parses_html_table PASSED
test_pitt_csc.py::test_scrape_pitt_csc_returns_empty_for_no_tables PASSED
test_pitt_csc.py::test_scrape_pitt_csc_handles_months PASSED
test_summer2027.py::test_scrape_summer2027_parses_markdown_table PASSED
test_summer2027.py::test_scrape_summer2027_returns_empty_for_no_table PASSED
7 passed
```

- [ ] **Step 2: Run Next.js tests**

```bash
npm test -- --watchAll=false --testPathPatterns="src/app/page.test.tsx|src/components/__tests__"
```

Expected output:
```
7 passed, 7 total
```

- [ ] **Step 3: Build the project**

```bash
npm run build
```

Expected: Build succeeds with no errors.

- [ ] **Step 4: Commit if tests pass**

```bash
git commit --allow-empty -m "test: verify all tests pass for Phase 1 scrapers"
```

---

### Task 10: Deploy to Vercel

- [ ] **Step 1: Push to GitHub**

```bash
git push
```

- [ ] **Step 2: Verify deployment**

Wait 30 seconds, then check:

```bash
sleep 30
curl -s "https://internship-website-gray.vercel.app/api/internships" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Total entries: {len(data)}')
# Check season distribution
from collections import Counter
seasons = Counter([e.get('season', 'unknown') for e in data])
for season, count in seasons.most_common():
    print(f'  {season}: {count}')
# Verify no duplicate IDs
ids = [e['id'] for e in data]
print(f'Unique IDs: {len(set(ids))} / {len(ids)}')
"
```

Expected output:
```
Total entries: ~500+
Summer 2026: ~200
Summer 2027: ~150
Fall 2026: ~50
Winter 2027: ~20
Spring 2027: ~20
Unique IDs: 500 / 500
```

- [ ] **Step 3: Final commit**

```bash
git commit --allow-empty -m "deploy: Phase 1 multi-source scraper expansion live"
```

---

## Self-Review

### Spec Coverage Check

| Spec Requirement | Implementing Task |
|-----------------|-------------------|
| Add `season` field to Internship type | Task 1 |
| Tag existing entries with "Summer 2026" | Task 2 |
| Create summer2027.py markdown parser | Task 3 |
| Create offseason.py HTML parser with per-term splitting | Task 5 |
| Extract run_scrapers.py orchestrator | Task 7 |
| Update GitHub Actions workflow | Task 8 |
| Unit tests for summer2027.py | Task 4 |
| Unit tests for offseason.py | Task 6 |
| Full test suite verification | Task 9 |
| Deploy to Vercel | Task 10 |

### Placeholder Scan

No TBDs, TODOs, or incomplete sections found. Every step contains actual code, exact commands, and expected output.

### Type Consistency

- `season` field added consistently across all scrapers (pitt_csc.py, summer2027.py, offseason.py)
- TypeScript type updated to match
- All entries use string values for season ("Summer 2026", "Summer 2027", "Fall 2026", etc.)

---

**Plan complete and saved to `docs/superpowers/plans/2025-07-25-multi-source-scraper-phase1.md`.**

**Two execution options:**

**1. Subagent-Driven (recommended)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
