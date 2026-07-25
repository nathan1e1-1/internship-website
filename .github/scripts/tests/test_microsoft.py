import pytest
from checkers.microsoft import check_microsoft

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_check_microsoft_finds_program(monkeypatch):
    html = """
    <html><body>
    <h2>Microsoft Explore — Summer 2026</h2>
    <p>Location: Redmond, WA</p>
    <a href="/explore">Apply Now</a>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.microsoft.requests.get", fake_get)

    result = check_microsoft()
    assert result is not None
    assert result["company"] == "Microsoft"
    assert "Explore" in result["title"]
    assert result["category"] == "top-tier"
    assert result["url"].startswith("http")

def test_check_microsoft_returns_none_when_not_found(monkeypatch):
    html = "<html><body><h1>All Careers</h1></body></html>"
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.microsoft.requests.get", fake_get)

    result = check_microsoft()
    assert result is None
