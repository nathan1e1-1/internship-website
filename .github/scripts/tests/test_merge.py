import pytest
from merge import merge_data
from datetime import datetime

def test_merge_deduplicates_by_id():
    bulk = [
        {"id": "nvidia-ignite-2026", "title": "NVIDIA Ignite", "company": "NVIDIA", "category": "general", "date_posted": "2025-07-10"},
        {"id": "google-step-2026", "title": "STEP", "company": "Google", "category": "general", "date_posted": "2025-07-10"},
    ]
    top_tier = [
        {"id": "nvidia-ignite-2026", "title": "NVIDIA Ignite", "company": "NVIDIA", "category": "top-tier", "date_posted": "2025-07-15"},
    ]
    result = merge_data(bulk, top_tier)
    assert len(result) == 2
    nvidia = [r for r in result if r["id"] == "nvidia-ignite-2026"][0]
    assert nvidia["category"] == "top-tier"

def test_merge_sorts_by_date_posted_descending():
    bulk = [
        {"id": "a", "date_posted": "2025-07-01"},
        {"id": "b", "date_posted": "2025-07-15"},
    ]
    result = merge_data(bulk, [])
    assert result[0]["id"] == "b"
    assert result[1]["id"] == "a"

def test_merge_filters_invalid_urls():
    bulk = [
        {"id": "a", "url": "not-a-url", "date_posted": "2025-07-01"},
        {"id": "b", "url": "https://valid.com", "date_posted": "2025-07-01"},
    ]
    result = merge_data(bulk, [])
    assert len(result) == 1
    assert result[0]["id"] == "b"

def test_merge_drops_entries_without_id():
    bulk = [
        {"id": "a", "date_posted": "2025-07-01"},
        {"title": "Missing ID", "date_posted": "2025-07-01"},
    ]
    result = merge_data(bulk, [])
    assert len(result) == 1
