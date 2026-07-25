import pytest
from scrapers.pitt_csc import scrape_pitt_csc

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_scrape_pitt_csc_parses_markdown_table(monkeypatch):
    markdown = """
| Company | Role | Location | Date Posted | Application |
|---|---|---|---|---|
| Acme | SWE Intern | Remote | July 1 | [Apply](https://acme.com) |
| Beta | Data Intern | NYC | July 2 | [Apply](https://beta.com) |
"""
    def fake_get(url, **kwargs):
        return FakeResponse(markdown)
    monkeypatch.setattr("scrapers.pitt_csc.requests.get", fake_get)

    result = scrape_pitt_csc("https://example.com/list.md")
    assert len(result) == 2
    assert result[0]["company"] == "Acme"
    assert result[0]["url"] == "https://acme.com"
    assert result[0]["type"] == "internship"
