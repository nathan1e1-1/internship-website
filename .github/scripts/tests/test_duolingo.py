import pytest
from checkers.duolingo import check_duolingo

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_check_duolingo_finds_program(monkeypatch):
    html = """
    <html><body>
    <h2>Duolingo Thrive — Summer 2026</h2>
    <p>Location: Pittsburgh, PA</p>
    <a href="/thrive">Apply Now</a>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.duolingo.requests.get", fake_get)

    result = check_duolingo()
    assert result is not None
    assert result["company"] == "Duolingo"
    assert "Thrive" in result["title"] or "Internship" in result["title"]
    assert result["category"] == "top-tier"
    assert result["url"].startswith("http")

def test_check_duolingo_returns_none_when_not_found(monkeypatch):
    html = "<html><body><h1>All Careers</h1></body></html>"
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.duolingo.requests.get", fake_get)

    result = check_duolingo()
    assert result is None
