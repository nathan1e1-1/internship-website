import pytest
from checkers.pinterest import check_pinterest

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_check_pinterest_finds_program(monkeypatch):
    html = """
    <html><body>
    <h2>Pinterest Engage — Summer 2026</h2>
    <p>Location: San Francisco, CA</p>
    <a href="/engage">Apply Now</a>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.pinterest.requests.get", fake_get)

    result = check_pinterest()
    assert result is not None
    assert result["company"] == "Pinterest"
    assert "Engage" in result["title"] or "Apprenticeship" in result["title"]
    assert result["category"] == "top-tier"
    assert result["url"].startswith("http")

def test_check_pinterest_returns_none_when_not_found(monkeypatch):
    html = "<html><body><h1>All Careers</h1></body></html>"
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.pinterest.requests.get", fake_get)

    result = check_pinterest()
    assert result is None
