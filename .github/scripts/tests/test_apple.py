import pytest
from checkers.apple import check_apple

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_check_apple_finds_program(monkeypatch):
    html = """
    <html><body>
    <h2>Apple Internship — Summer 2026</h2>
    <p>Location: Cupertino, CA</p>
    <a href="/intern">Apply Now</a>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.apple.requests.get", fake_get)

    result = check_apple()
    assert result is not None
    assert result["company"] == "Apple"
    assert "Internship" in result["title"]
    assert result["category"] == "top-tier"
    assert result["url"].startswith("http")

def test_check_apple_returns_none_when_not_found(monkeypatch):
    html = "<html><body><h1>All Jobs</h1></body></html>"
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.apple.requests.get", fake_get)

    result = check_apple()
    assert result is None
