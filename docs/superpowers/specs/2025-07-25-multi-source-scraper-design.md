# Multi-Source Scraper Expansion Design

**Date:** 2025-07-25
**Scope:** Add Summer 2027 repo, Off-Season internships, and 20 top-tier company checkers

---

## Background

The internship board currently serves 217 unique listings from:
- `SimplifyJobs/Summer2026-Internships` (HTML table parser)
- 9 individual top-tier company checkers

This design expands to ~500-700 listings by adding:
- Summer 2027 internships (`vanshb03/Summer2027-Internships`)
- Off-season internships (Fall 2026, Winter 2027, Spring 2027)
- 20 additional top-tier checkers

---

## Data Model Change

Add optional `season` string to the `Internship` type:

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
  season?: string;        // NEW: "Summer 2026", "Summer 2027", "Fall 2026", etc.
  eligibility?: string;
  date_posted?: string;
  deadline?: string;
  notes?: string;
  date_scraped: string;
}
```

- `season` is **not displayed on the frontend** in this phase
- Existing entries backfilled with `"Summer 2026"`

---

## New Scraper Modules

### summer2027.py

**Source:** `https://raw.githubusercontent.com/vanshb03/Summer2027-Internships/main/README.md`

**Format:** Markdown tables (`| Company | Role | Location | Link | Date Posted |`)

**Parsing:**
- Fetch raw markdown, parse table rows
- Extract apply URL from first `<a href="...">` in the cell
- Handle `↳` continuation rows
- Extract emoji notes (🛂, 🇺🇸, 🔒)
- Convert `Jul 24` format to `YYYY-MM-DD`

**ID generation:** Same hash-based approach as `pitt_csc.py`

**Deduplication:** By `(company, title, location)` keeping first occurrence

**Tag:** `category: "general"`, `season: "Summer 2027"`

### offseason.py

**Source:** `https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README-Off-Season.md`

**Format:** HTML tables with extra **"Terms"** column

**Parsing:**
- Reuse existing BeautifulSoup HTML table parsing from `pitt_csc.py`
- Extract "Terms" column (e.g., "Fall 2026", "Fall 2026, Winter 2027, Spring 2027")
- **Per-term entries:** If multiple terms, create **one entry per term**
- Handle `↳` continuation rows, emoji extraction, URL extraction exactly like current parser

**Tag:** `category: "general"`, `season: <term>`

### pitt_csc.py update

- Add `season: "Summer 2026"` to existing entries for consistency

---

## Workflow Refactor

**Before:** Inline 40-line Python block in `.github/workflows/scrape.yml`

**After:** Extract to `.github/scripts/run_scrapers.py`

```python
# run_scrapers.py - orchestrates all scrapers
import sys
from scrapers.pitt_csc import scrape_pitt_csc
from scrapers.summer2027 import scrape_summer2027
from scrapers.offseason import scrape_offseason
from checkers.greenhouse import *  # Batch 1-2
from checkers.html_fallback import *  # Batch 3-4
from merge import merge_data, write_json

def main():
    bulk = []
    sources = [
        ("Summer 2026", scrape_pitt_csc, "..."),
        ("Summer 2027", scrape_summer2027, "..."),
        ("Off-Season", scrape_offseason, "..."),
    ]
    for name, scraper, url in sources:
        try:
            entries = scraper(url)
            bulk.extend(entries)
        except Exception as e:
            print(f"{name} error: {e}", file=sys.stderr)
    
    top_tier = []
    for checker in ALL_CHECKERS:
        try:
            result = checker()
            if result:
                top_tier.append(result)
        except Exception as e:
            print(f"{checker.__name__} error: {e}", file=sys.stderr)
    
    merged = merge_data(bulk, top_tier)
    write_json(merged, "data/internships.json")
    print(f"Wrote {len(merged)} total entries")

if __name__ == "__main__":
    main()
```

**YAML change:**
```yaml
- name: Run scrapers
  run: |
    cd .github/scripts
    python run_scrapers.py
```

---

## Top-Tier Checkers (20 companies)

### Greenhouse API Tier (10 companies)

These expose `boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true` — a **public, unauthenticated JSON API**.

**Reusable checker pattern:**
```python
def check_greenhouse_company(board_slug: str, company_name: str, program_name: str) -> dict | None:
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_slug}/jobs?content=true"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    jobs = resp.json().get('jobs', [])
    
    intern_keywords = ['intern', 'internship', 'university', 'new grad']
    intern_jobs = [j for j in jobs if any(kw in j.get('title', '').lower() for kw in intern_keywords)]
    
    if intern_jobs:
        job = intern_jobs[0]
        return {
            "id": f"{company_name.lower().replace(' ', '-')}-intern-{datetime.now().year + 1}",
            "title": job['title'],
            "company": company_name,
            "type": "internship",
            "category": "top-tier",
            "url": job.get('absolute_url', ''),
            "location": job.get('location', {}).get('name', 'TBD'),
            "work_type": "hybrid",
            "date_scraped": datetime.now().isoformat()[:10],
        }
    return None
```

| Company | Board Slug | Verification Status |
|---------|-----------|-------------------|
| Stripe | `stripe` | ✅ API works |
| Spotify | `spotify` | ✅ API works |
| Dropbox | `dropbox` | ✅ API works |
| Databricks | `databricks` | ✅ API works (2 live internships) |
| Palantir | `palantir` | ✅ API works |
| Figma | `figma` | ✅ API works |
| Snowflake | `snowflake` | ✅ API works |
| Notion | `notion` | ✅ API works |
| Datadog | `datadog` | ✅ API works |
| Pinterest | `pinterest` | Existing checker already uses this |

### HTML Fallback Tier (10 companies)

No public API discovered. Use existing keyword-search pattern.

| Company | Careers URL | Search Keywords |
|---------|------------|----------------|
| Netflix | `jobs.netflix.com/jobs` | `intern`, `software engineer intern` |
| Salesforce | `salesforce.wd1.myworkdayjobs.com` | `futureforce`, `intern` |
| Adobe | `careers.adobe.com` | `university`, `intern` |
| Intel | `jobs.intel.com` | `student`, `intern` |
| AMD | `careers.amd.com` | `intern` |
| Qualcomm | `qualcomm.wd5.myworkdayjobs.com` | `university`, `intern` |
| Anthropic | `jobs.ashbyhq.com/anthropic` | `intern`, `residency` |
| OpenAI | `openai.com/careers` | `intern`, `residency` |
| Airbnb | `airbnb.com/careers` | `internship`, `university` |
| Mistral | `jobs.lever.co/mistralai` (unconfirmed) | `intern` |

### End-to-End Verification

**Databricks** is built and verified first because:
- Greenhouse API returns live data today (Product Management Intern Summer 2027)
- Confirms the API pattern works end-to-end
- Provides a real test case for the normalize/merge pipeline

---

## Merge & Deduplication

No changes to `merge.py` core logic. The existing dict-based merge by `id` still works because:
- Different sources use the same hash-based ID generation
- Summer 2026 and Summer 2027 entries with same company+title will have different IDs (different `date_posted` → different hash)
- Off-season per-term entries are naturally unique

**Expected total:** 217 (current) + ~150 (Summer 2027) + ~150 (Off-Season) + ~20 top-tier = **~537 listings**

---

## Testing Plan

- Unit test for `summer2027.py` — mock markdown table, verify parsing
- Unit test for `offseason.py` — mock HTML table with Terms column
- One test per new checker (mock HTTP response)
- Integration test: merge handles 3-source data without collisions
- End-to-end: Verify Databricks checker returns real data from live API

---

## Frontend Impact

**None in this phase.** The `season` field exists in the data but is not rendered.

Future phases can add:
- Season filter dropdown
- Season badge on cards
- Separate sections for "Summer 2027" vs "Fall 2026"

---

## Implementation Phases

| Phase | Deliverables | Est. Listings Added |
|-------|-----------|-------------------|
| **Phase 1** | `summer2027.py`, `offseason.py` (per-term), `run_scrapers.py`, `season` field in types, workflow refactor | +300-400 (bulk) |
| **Phase 2** | Greenhouse checkers (Stripe, Spotify, Dropbox, Databricks, Palantir, Figma, Snowflake, Notion, Datadog) + end-to-end Databricks verification | +9 featured |
| **Phase 3** | HTML fallback checkers Batch 1 (Netflix, Salesforce, Adobe, Intel, AMD, Qualcomm) | +6 featured |
| **Phase 4** | HTML fallback checkers Batch 2 (Anthropic, OpenAI, Airbnb, Mistral) + final integration test + visual polish | +4 featured |

---

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Greenhouse API changes/breaks | Low | API v1 stable for years; fallback to HTML if needed |
| HTML structure changes on Workday/Lever | Medium | Tests catch breakage; checker returns None gracefully |
| Summer 2027 repo format changes | Medium | Parser is defensive; logs errors without crashing |
| Total entries >1K | Medium | Monitor Vercel cold-start; paginate API if needed |

---

## Decisions Log

1. **Off-Season term handling:** Per-term entries (Option A). Multiple terms create multiple entries with unique IDs.
2. **Checker approach:** Hybrid. Greenhouse API for 10 companies, HTML keyword search for 10 companies.
3. **End-to-end verification:** Databricks first (has live internship postings today).
4. **Home Depot / Walmart:** Excluded from top-tier; will come through bulk scrape only.
5. **External aggregators (Handshake/LinkedIn/Indeed):** Skipped — require auth/anti-bot measures not suitable for portfolio project.
