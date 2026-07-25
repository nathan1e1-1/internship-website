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
| Gamma LLC | Frontend Intern | Remote in US | <a href="https://apply.gamma.com">Apply</a> | Jul 21 |
"""
    def fake_get(url, **kwargs):
        return FakeResponse(markdown)
    monkeypatch.setattr("scrapers.summer2027.requests.get", fake_get)

    result = scrape_summer2027("https://example.com/summer2027.md")
    assert len(result) == 4

    # First entry
    assert result[0]["company"] == "Acme Corp"
    assert result[0]["title"] == "Software Engineer Intern"
    assert result[0]["url"] == "https://apply.acme.com"
    assert result[0]["season"] == "Summer 2027"
    assert result[0]["work_type"] == "remote"
    assert result[0]["date_posted"] is not None

    # Second entry with emoji
    assert result[1]["company"] == "Beta Inc"
    assert result[1]["title"] == "Data Intern"
    assert result[1]["notes"] == "Advanced degree required"

    # Continuation row
    assert result[2]["company"] == "Beta Inc"
    assert result[2]["title"] == "ML Intern"
    assert result[2]["url"] == "https://apply.beta2.com"

    # Remote entry
    assert result[3]["company"] == "Gamma LLC"
    assert result[3]["work_type"] == "remote"

def test_scrape_summer2027_returns_empty_for_no_table(monkeypatch):
    markdown = "# No internships here\n\nJust some text."
    def fake_get(url, **kwargs):
        return FakeResponse(markdown)
    monkeypatch.setattr("scrapers.summer2027.requests.get", fake_get)

    result = scrape_summer2027("https://example.com/empty.md")
    assert result == []
