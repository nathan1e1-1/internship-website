import pytest
from checkers.google import check_google

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_check_google_finds_program(monkeypatch):
    html = """
    <html><body>
    <h2>STEP Internship — Summer 2026</h2>
    <p>Location: Mountain View, CA</p>
    <a href="/step">Apply Now</a>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.google.requests.get", fake_get)

    result = check_google()
    assert result is not None
    assert result["company"] == "Google"
    assert "STEP" in result["title"]
    assert result["category"] == "top-tier"
    assert result["url"].startswith("http")

def test_check_google_returns_none_when_not_found(monkeypatch):
    html = "<html><body><h1>All Programs</h1></body></html>"
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.google.requests.get", fake_get)

    result = check_google()
    assert result is None
