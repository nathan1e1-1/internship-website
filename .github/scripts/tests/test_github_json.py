import pytest
from scrapers.github_json import scrape_github_json

class FakeResponse:
    def __init__(self, json_data, status=200):
        self._json = json_data
        self.status_code = status
    def json(self):
        return self._json
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_scrape_github_json_normalizes_entries(monkeypatch):
    raw = [
        {
            "company": "Acme",
            "title": "SWE Intern",
            "location": "Remote",
            "url": "https://acme.com",
            "date_posted": "2025-07-01"
        }
    ]
    def fake_get(url, **kwargs):
        return FakeResponse(raw)
    monkeypatch.setattr("scrapers.github_json.requests.get", fake_get)

    result = scrape_github_json("https://example.com/internships.json")
    assert len(result) == 1
    assert result[0]["company"] == "Acme"
    assert result[0]["type"] == "internship"
    assert result[0]["category"] == "general"
    assert "id" in result[0]
    assert "date_scraped" in result[0]
