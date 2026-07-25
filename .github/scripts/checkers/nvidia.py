import requests
from datetime import datetime
from bs4 import BeautifulSoup

def check_nvidia() -> dict:
    url = "https://www.nvidia.com/en-us/about-nvidia/careers/"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    if "ignite" not in text.lower():
        return None
    title = "NVIDIA Ignite"
    for heading in soup.find_all(["h1", "h2", "h3"]):
        if "ignite" in heading.get_text(strip=True).lower():
            title = heading.get_text(strip=True)
            break
    location = "Santa Clara, CA (Multiple)"
    deadline = None
    apply_url = "https://www.nvidia.com/en-us/about-nvidia/careers/ignite/"
    return {
        "id": "nvidia-ignite-" + str(datetime.now().year + 1),
        "title": title,
        "company": "NVIDIA",
        "type": "internship",
        "category": "top-tier",
        "url": apply_url,
        "location": location,
        "work_type": "hybrid",
        "date_scraped": datetime.now().isoformat()[:10],
    }
