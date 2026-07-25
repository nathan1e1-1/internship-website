import requests
from datetime import datetime

def check_greenhouse_company(board_slug: str, company_name: str, program_name: str = None) -> dict | None:
    """Check a Greenhouse-hosted careers page for internship listings.
    
    Args:
        board_slug: The Greenhouse board slug (e.g., 'stripe', 'databricks')
        company_name: Human-readable company name
        program_name: Optional specific program name to use in the title
    
    Returns:
        Normalized internship dict if an intern job is found, else None
    """
    url = f"https://boards-api.greenhouse.io/v1/boards/{board_slug}/jobs?content=true"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    jobs = resp.json().get('jobs', [])
    
    intern_keywords = ['intern', 'internship', 'university', 'new grad']
    intern_jobs = [j for j in jobs if any(kw in j.get('title', '').lower() for kw in intern_keywords)]
    
    if intern_jobs:
        job = intern_jobs[0]
        title = program_name or job['title']
        year = str(datetime.now().year + 1)
        company_slug = company_name.lower().replace(' ', '-').replace(',', '')[:20]
        
        return {
            "id": f"{company_slug}-intern-{year}",
            "title": title,
            "company": company_name,
            "type": "internship",
            "category": "top-tier",
            "url": job.get('absolute_url', ''),
            "location": job.get('location', {}).get('name', 'TBD'),
            "work_type": "hybrid",
            "season": f"Summer {year}",
            "date_scraped": datetime.now().isoformat()[:10],
        }
    return None
