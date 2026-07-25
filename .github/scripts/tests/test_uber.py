import pytest
from checkers.uber import check_uber

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_check_uber_finds_program(monkeypatch):
    html = """
    <html><body>
    <h2>UberSTAR — Summer 2026</h2>
    <p>Location: San Francisco, CA</p>
    <a href="/uberstar">Apply Now</a>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.uber.requests.get", fake_get)

    result = check_uber()
    assert result is not None
    assert result["company"] == "Uber"
    assert "UberSTAR" in result["title"] or "SWE" in result["title"]
    assert result["category"] == "top-tier"
    assert result["url"].startswith("http")

def test_check_uber_returns_none_when_not_found(monkeypatch):
    html = "<html><body><h1>All Listings</h1></body></html>"
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.uber.requests.get", fake_get)

    result = check_uber()
    assert result is None
