import pytest
from scrapers.offseason import scrape_offseason

class FakeResponse:
    def __init__(self, text, status=200):
        self.text = text
        self.status_code = status
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception("HTTP Error")

def test_scrape_offseason_parses_html_table_with_terms(monkeypatch):
    html = """
    <html><body>
    <table>
      <thead><tr><th>Company</th><th>Role</th><th>Location</th><th>Terms</th><th>Application</th><th>Age</th></tr></thead>
      <tbody>
        <tr>
          <td><strong><a href="https://acme.com">Acme</a></strong></td>
          <td>SWE Intern</td>
          <td>Remote</td>
          <td>Fall 2026</td>
          <td><a href="https://apply.acme.com">Apply</a></td>
          <td>1d</td>
        </tr>
        <tr>
          <td><strong><a href="https://beta.com">Beta</a></strong></td>
          <td>Data Intern</td>
          <td>NYC</td>
          <td>Fall 2026, Winter 2027, Spring 2027</td>
          <td><a href="https://apply.beta.com">Apply</a></td>
          <td>2w</td>
        </tr>
        <tr>
          <td>↳</td>
          <td>ML Intern</td>
          <td>NYC</td>
          <td>Fall 2026</td>
          <td><a href="https://apply.beta2.com">Apply</a></td>
          <td>2w</td>
        </tr>
      </tbody>
    </table>
    </body></html>
    """
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("scrapers.offseason.requests.get", fake_get)

    result = scrape_offseason("https://example.com/offseason.html")
    
    # Acme: 1 entry (Fall 2026)
    acme_entries = [e for e in result if e["company"] == "Acme"]
    assert len(acme_entries) == 1
    assert acme_entries[0]["season"] == "Fall 2026"
    assert acme_entries[0]["title"] == "SWE Intern"
    assert acme_entries[0]["work_type"] == "remote"

    # Beta: 3 entries (one per term)
    beta_entries = [e for e in result if e["company"] == "Beta" and e["title"] == "Data Intern"]
    assert len(beta_entries) == 3
    seasons = sorted([e["season"] for e in beta_entries])
    assert seasons == ["Fall 2026", "Spring 2027", "Winter 2027"]

    # Beta continuation row: 1 entry
    beta_ml_entries = [e for e in result if e["company"] == "Beta" and e["title"] == "ML Intern"]
    assert len(beta_ml_entries) == 1
    assert beta_ml_entries[0]["season"] == "Fall 2026"

def test_scrape_offseason_returns_empty_for_no_tables(monkeypatch):
    html = "<html><body><h1>No tables</h1></body></html>"
    def fake_get(url, **kwargs):
        return FakeResponse(html)
    monkeypatch.setattr("scrapers.offseason.requests.get", fake_get)

    result = scrape_offseason("https://example.com/empty.html")
    assert result == []
