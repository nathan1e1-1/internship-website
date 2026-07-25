import pytest
from checkers.amazon import check_amazon

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_check_amazon_finds_program(monkeypatch):
    html = """
    <html><body>
    <h2>Amazon Propel — Summer 2026</h2>
    <p>Location: Seattle, WA</p>
    <a href="/propel">Apply Now</a>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.amazon.requests.get", fake_get)

    result = check_amazon()
    assert result is not None
    assert result["company"] == "Amazon"
    assert "Propel" in result["title"] or "University" in result["title"]
    assert result["category"] == "top-tier"
    assert result["url"].startswith("http")

def test_check_amazon_returns_none_when_not_found(monkeypatch):
    html = "<html><body><h1>All Teams</h1></body></html>"
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.amazon.requests.get", fake_get)

    result = check_amazon()
    assert result is None
