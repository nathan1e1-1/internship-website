import pytest
from checkers.nvidia import check_nvidia

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_check_nvidia_finds_ignite(monkeypatch):
    html = """
    <html><body>
    <h2>NVIDIA Ignite — Summer 2026</h2>
    <p>Location: Santa Clara, CA</p>
    <p>Apply by October 1, 2025</p>
    <a href="/careers/ignite">Apply Now</a>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.nvidia.requests.get", fake_get)

    result = check_nvidia()
    assert result is not None
    assert result["company"] == "NVIDIA"
    assert "Ignite" in result["title"]
    assert result["category"] == "top-tier"
    assert result["url"].startswith("http")

def test_check_nvidia_returns_none_when_not_found(monkeypatch):
    html = "<html><body><h1>All Careers</h1></body></html>"
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("checkers.nvidia.requests.get", fake_get)

    result = check_nvidia()
    assert result is None
