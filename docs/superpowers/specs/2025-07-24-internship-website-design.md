# Internship Board Website — Design Document

**Date:** 2025-07-24
**Status:** Approved
**Approach:** Static JSON + ISR (Approach A)

---

## 1. Overview

A simple, fast, and always-updating website that aggregates internship and fellowship opportunities for students. The site prioritizes top-tier programs (NVIDIA Ignite, Google STEP, Microsoft Explore, etc.) in a featured section, while maintaining a complete, filterable list of all opportunities.

### Success Criteria
- Users can discover internships within seconds of landing on the page
- Top-tier programs are visually prominent and easy to find
- Data refreshes automatically every day without manual intervention
- The site loads fast, works on mobile, and requires zero backend infrastructure cost

---

## 2. Architecture

### 2.1 System Diagram

```
GitHub Actions (Daily @ 06:00 UTC)
├─ Bulk Scrapers (Pitt CSC, Simplify API, GitHub JSON repos)
├─ Top-Tier Checkers (NVIDIA, Google, Microsoft, Meta, Apple, Amazon, Pinterest, Duolingo, Uber)
└─ Merge & Normalize → Commit data/internships.json

GitHub Repository
└─ data/internships.json

Vercel (Next.js 14+ App Router)
├─ ISR: Page regenerates every 1 hour
├─ Static API: /api/internships serves the JSON file
└─ React Frontend (Featured Section + Filters + List)
```

### 2.2 Key Decisions

- **Next.js 14+ App Router** with Incremental Static Regeneration (`revalidate: 3600`)
- **Static JSON** committed to the repo by GitHub Actions — no external database
- **Client-side fetch** from `/api/internships` after initial page load so filters use fresh data without waiting for ISR
- **Python scrapers** in `.github/scripts/` using `requests` and `BeautifulSoup`
- **Vercel Hobby tier** — free, sufficient for static site + ISR

---

## 3. Data Model

### 3.1 Internship Entry Schema

```json
{
  "id": "nvidia-ignite-2026",
  "title": "NVIDIA Ignite",
  "company": "NVIDIA",
  "type": "internship",
  "category": "top-tier",
  "url": "https://nvidia.com/...",
  "location": "Santa Clara, CA (Remote available)",
  "work_type": "hybrid",
  "eligibility": "Sophomores and Juniors",
  "date_posted": "2025-07-15",
  "deadline": "2025-10-01",
  "notes": "12-week summer program focused on AI/ML. Must be enrolled in BS/MS program.",
  "date_scraped": "2025-07-24"
}
```

### 3.2 Field Definitions

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Deterministic slug: `company-title-year` used for deduplication and stable URLs |
| `title` | string | Yes | Program title (e.g., "NVIDIA Ignite") |
| `company` | string | Yes | Company name |
| `type` | string | Yes | `internship` \| `fellowship` \| `program` |
| `category` | string | Yes | `top-tier` (featured) \| `general` (main list) |
| `url` | string | Yes | Direct application or program page link |
| `location` | string | Yes | City, state, or "Remote" / "Multiple Locations" |
| `work_type` | string | Yes | `remote` \| `hybrid` \| `in-person` |
| `eligibility` | string | No | Who can apply (e.g., "Freshmen and Sophomores") |
| `date_posted` | string (ISO date) | No | When the posting was published |
| `deadline` | string (ISO date) | No | Application deadline. Omitted if unknown |
| `notes` | string | No | Important details (duration, requirements, etc.) |
| `date_scraped` | string (ISO date) | Yes | When we last verified this entry |

### 3.3 File Format

- `data/internships.json` contains a single JSON array
- Sorted by `date_posted` descending (most recent first)
- Top-tier entries appear in both the featured section and the main list
- Missing `deadline` → UI renders "Deadline TBD" with muted styling

---

## 4. Scraping Strategy

### 4.1 Bulk Sources

| Source | Method | Output |
|---|---|---|
| Pitt CSC Internship List | Scrape markdown/table from GitHub repo or wiki | Array of entries |
| Simplify Open API | HTTP GET with optional API key | Array of entries |
| Community GitHub JSON repos | Fetch raw JSON (e.g., `SimplifyJobs/Summer2026-Internships`) | Array of entries |

**Normalizer:** Each bulk scraper normalizes its raw output into our schema before returning.

### 4.2 Top-Tier Individual Checkers

Each checker is a standalone Python script that:

1. Fetches the specific company's careers / university program page
2. Searches for program-specific keywords in titles and descriptions
3. Extracts available fields (title, location, deadline if visible, URL)
4. Normalizes to our schema
5. Returns one entry (or `null` if not found / closed)

**Top-tier programs monitored:**
- NVIDIA Ignite
- Google STEP (Student Training in Engineering Program)
- Microsoft Explore
- Meta University
- Apple student programs (e.g., ADP, MLWF)
- Amazon Propel / UII (University Internship Initiative)
- Pinterest Engage / Apprenticeship
- Duolingo Thrive / Internship
- UberSTAR / SWE Internship (underclassmen-focused)

### 4.3 Merge Pipeline

```
1. Collect all bulk scraper outputs (arrays)
2. Collect all top-tier checker outputs (individual entries)
3. Deduplicate by `id` — top-tier entries override bulk entries for the same program
4. Sort by `date_posted` descending
5. Write to `data/internships.json`
6. Git commit only if the file content changed
```

### 4.4 GitHub Action Schedule

- **Trigger:** Daily at `06:00 UTC` via cron schedule
- **Manual trigger:** `workflow_dispatch` enabled for testing
- **Runner:** `ubuntu-latest`
- **Steps:** checkout → setup Python 3.11 → install deps → run all scrapers/checkers → merge → commit if changed

---

## 5. Frontend Design

### 5.1 Page Layout (Single Page)

```
┌─────────────────────────────────────────┐
│  Header                                 │
│  Title + Subtitle + Last Updated        │
├─────────────────────────────────────────┤
│  Featured Section (Top-Tier Cards)    │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐       │
│  │NVIDIA│ │Google│ │Microsoft│ │Meta│  │
│  │Ignite│ │ STEP │ │Explore │ │ Uni│  │
│  └─────┘ └─────┘ └─────┘ └─────┘       │
├─────────────────────────────────────────┤
│  Filter Bar                             │
│  [Company ▼] [Location ▼] [Type ▼] [Work▼] [Clear] │
├─────────────────────────────────────────┤
│  Main List (All Internships)            │
│  ┌────────────────────────────────────┐ │
│  │ Title | Company | Location | Type  │ │
│  │ Date Posted | Deadline | [Apply]   │ │
│  └────────────────────────────────────┘ │
│  ...                                    │
├─────────────────────────────────────────┤
│  Footer                                 │
│  "Updated daily via automated scraping" │
└─────────────────────────────────────────┘
```

### 5.2 Featured Section

- Horizontal scrollable row of cards (or 2-3 column grid on desktop)
- Each card: **Company name**, **Program title**, **Deadline badge**
- Deadline badge color coding:
  - **Red:** < 14 days remaining
  - **Yellow:** < 30 days remaining
  - **Neutral:** 30+ days or no deadline
- Direct **"Apply"** button linking to the URL (opens in new tab)

### 5.3 Filter Bar

- Dropdown filters (client-side, no page reload):
  - **Company:** All unique companies from the dataset
  - **Location:** All unique locations
  - **Type:** `internship`, `fellowship`, `program`
  - **Work Type:** `remote`, `hybrid`, `in-person`
- **"Clear all"** link to reset filters
- Filters apply instantly after selection

### 5.4 Main List

- Default sort: `date_posted` descending (most recent first)
- Each entry shows:
  - **Title** + **Company**
  - **Location** + **Work Type** badge
  - **Type** badge (internship/fellowship/program)
  - **Date Posted**
  - **Deadline** (with badge color if urgent)
  - **"Apply"** button (external link, new tab)
  - **Expandable notes** — collapsed by default, click to show important details
- Mobile: cards stack vertically; filters collapse into a drawer

### 5.5 Styling Principles

- **Minimal and sleek:** whitespace-driven, no heavy shadows or gradients
- **Tailwind CSS** utility classes
- **No heavy UI library** — custom lightweight components
- Color palette: neutral grays + one accent color for CTAs and badges

---

## 6. Error Handling

### 6.1 Scraper Failures

- A single failed scraper or checker does **not** fail the entire GitHub Action
- Errors are logged to GitHub Actions output for inspection
- Existing `data/internships.json` is **never overwritten** with partial or broken data
- The merge script only commits if the final output is valid JSON and non-empty

### 6.2 Top-Tier Checker Failures

- If a checker fails (page changed, network error), it returns `null`
- Other checkers continue unaffected
- The existing entry for that program (if any) is preserved from the previous run

### 6.3 Frontend Edge Cases

| Scenario | Behavior |
|---|---|
| Empty or missing `data/internships.json` | Show "No internships found right now. Check back tomorrow!" |
| `/api/internships` fails to load | Static ISR page still renders with last known data; filters disabled |
| Missing `deadline` | Render "Deadline TBD" with muted gray styling |
| Missing `location` | Render "Location TBD" with muted gray styling |
| Very long `notes` | Truncate with "Show more" expand button |
| Invalid URL | Filtered out during merge; never shown to users |

---

## 7. Project Structure

```
internship-website/
├── .github/
│   ├── workflows/
│   │   └── scrape.yml              # GitHub Action: daily scrape + commit
│   └── scripts/
│       ├── scrapers/
│       │   ├── __init__.py
│       │   ├── pitt_csc.py         # Pitt CSC scraper
│       │   ├── simplify.py         # Simplify API scraper
│       │   └── github_json.py      # Community GitHub repo scraper
│       ├── checkers/
│       │   ├── __init__.py
│       │   ├── nvidia.py
│       │   ├── google.py
│       │   ├── microsoft.py
│       │   ├── meta.py
│       │   ├── apple.py
│       │   ├── amazon.py
│       │   ├── pinterest.py
│       │   ├── duolingo.py
│       │   └── uber.py
│       ├── merge.py               # Deduplicate + normalize + sort
│       └── requirements.txt       # Python deps (requests, beautifulsoup4)
├── data/
│   └── internships.json           # Generated by GitHub Action
├── src/
│   ├── app/
│   │   ├── page.tsx               # Main page (Featured + List + Filters)
│   │   ├── layout.tsx             # Root layout with metadata
│   │   └── api/
│   │       └── internships/
│   │           └── route.ts       # Static API: serves data/internships.json
│   └── components/
│       ├── Header.tsx
│       ├── FeaturedSection.tsx
│       ├── FilterBar.tsx
│       ├── InternshipList.tsx
│       ├── InternshipCard.tsx
│       └── Footer.tsx
├── public/
│   └── (static assets)
├── next.config.js
├── tailwind.config.js
├── tsconfig.json
└── package.json
```

---

## 8. Deployment & Environment

### 8.1 Vercel

- GitHub repo connected to Vercel for automatic deploys on every push
- **No environment variables required** for the frontend (reads committed JSON)
- ISR revalidation: `3600` seconds (1 hour)
- Free Hobby tier is sufficient

### 8.2 GitHub Action

```yaml
on:
  schedule:
    - cron: '0 6 * * *'   # Daily at 06:00 UTC
  workflow_dispatch:         # Manual trigger for testing
```

### 8.3 Secrets

| Secret | Required | Purpose |
|---|---|---|
| `SIMPLIFY_API_KEY` | Conditional | Only if Simplify API requires authentication in practice. If not available, scraper falls back gracefully. |

No other secrets needed for basic HTTP scraping.

---

## 9. Future Considerations (Out of Scope)

The following are explicitly **not** part of this design but may be added later:

- User accounts / saved internships
- Email alerts / subscriptions
- Pagination (only needed if list grows beyond ~500 entries)
- Dark mode toggle
- Search-as-you-type across all text fields
- Admin dashboard for manual overrides

---

## 10. Open Questions / Risks

| Risk | Mitigation |
|---|---|
| Simplify API requires paid key | Fall back to GitHub JSON repos and Pitt CSC only |
| Company career pages change structure | Checkers log failures; manual intervention if a checker stays broken for > 7 days |
| GitHub Actions free tier has 2,000 min/month limit | Daily run ~2-5 min = well within limits |
| Vercel ISR on free tier has limits | Hourly revalidation is well within free limits |
