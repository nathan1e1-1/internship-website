import pytest
from scrapers.pitt_csc import scrape_pitt_csc

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_scrape_pitt_csc_parses_html_table(monkeypatch):
    html = """
    <html><body>
    <table>
      <thead><tr><th>Company</th><th>Role</th><th>Location</th><th>Application</th><th>Age</th></tr></thead>
      <tbody>
        <tr>
          <td><strong><a href="https://acme.com">Acme</a></strong></td>
          <td>SWE Intern</td>
          <td>Remote</td>
          <td><a href="https://apply.acme.com">Apply</a></td>
          <td>1d</td>
        </tr>
        <tr>
          <td><strong><a href="https://beta.com">Beta 🎓</a></strong></td>
          <td>Data Intern</td>
          <td>NYC</td>
          <td><a href="https://apply.beta.com">Apply</a></td>
          <td>2w</td>
        </tr>
      </tbody>
    </table>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("scrapers.pitt_csc.requests.get", fake_get)

    result = scrape_pitt_csc("https://example.com/list.html")
    assert len(result) == 2
    assert result[0]["company"] == "Acme"
    assert result[0]["title"] == "SWE Intern"
    assert result[0]["url"] == "https://apply.acme.com"
    assert result[0]["type"] == "internship"
    assert result[0]["date_posted"] is not None  # 1d should parse
    
    assert result[1]["company"] == "Beta"
    assert result[1]["notes"] == "Advanced degree required"
    assert result[1]["date_posted"] is not None  # 2w should parse

def test_scrape_pitt_csc_returns_empty_for_no_tables(monkeypatch):
    html = "<html><body><h1>No tables here</h1></body></html>"
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("scrapers.pitt_csc.requests.get", fake_get)

    result = scrape_pitt_csc("https://example.com/empty.html")
    assert result == []

def test_scrape_pitt_csc_handles_months(monkeypatch):
    html = """
    <html><body>
    <table>
      <thead><tr><th>Company</th><th>Role</th><th>Location</th><th>Application</th><th>Age</th></tr></thead>
      <tbody>
        <tr>
          <td><strong><a href="https://later.com">Later</a></strong></td>
          <td>AI Automation Engineer Co-op</td>
          <td>Vancouver, BC</td>
          <td><a href="https://apply.later.com">Apply</a></td>
          <td>1mo</td>
        </tr>
      </tbody>
    </table>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("scrapers.pitt_csc.requests.get", fake_get)

    result = scrape_pitt_csc("https://example.com/list.html")
    assert len(result) == 1
    assert result[0]["company"] == "Later"
    assert result[0]["date_posted"] is not None  # 1mo should parse
