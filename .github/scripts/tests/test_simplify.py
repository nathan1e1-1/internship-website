import pytest
from scrapers.simplify import scrape_simplify

class FakeResponse:
    def __init__(self, json_data, status=200):
        self._json = json_data
        self.status_code = status
    def json(self):
        return self._json
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_scrape_simplify_with_api_key(monkeypatch):
    raw = {
        "data": [
            {
                "company": "Acme",
                "title": "SWE Intern",
                "location": "Remote",
                "url": "https://acme.com",
                "date_posted": "2025-07-01",
                "work_type": "remote"
            }
        ]
    }
    def fake_get(url, **kwargs):
        return FakeResponse(raw)
    monkeypatch.setattr("scrapers.simplify.requests.get", fake_get)

    result = scrape_simplify("https://api.simplify.com/jobs", api_key="test-key")
    assert len(result) == 1
    assert result[0]["company"] == "Acme"
    assert result[0]["work_type"] == "remote"
    assert result[0]["category"] == "general"

def test_scrape_simplify_without_key(monkeypatch):
    def fake_get(url, **kwargs):
        return FakeResponse({"data": []})
    monkeypatch.setattr("scrapers.simplify.requests.get", fake_get)

    result = scrape_simplify("https://api.simplify.com/jobs")
    assert result == []
