import pytest
from checkers.meta import check_meta

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_check_meta_finds_program(monkeypatch):
    html = """
    <html><body>
    <h2>Meta University — Summer 2026</h2>
    <p>Location: Menlo Park, CA</p>
    <a href="/university">Apply Now</a>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.meta.requests.get", fake_get)

    result = check_meta()
    assert result is not None
    assert result["company"] == "Meta"
    assert "University" in result["title"]
    assert result["category"] == "top-tier"
    assert result["url"].startswith("http")

def test_check_meta_returns_none_when_not_found(monkeypatch):
    html = "<html><body><h1>All Jobs</h1></body></html>"
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.meta.requests.get", fake_get)

    result = check_meta()
    assert result is None
