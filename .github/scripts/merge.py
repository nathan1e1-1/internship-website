import json
import re

def _is_valid_url(url: str) -> bool:
    if not url:
        return True
    return bool(re.match(r'^https?://', str(url)))

def _has_required_fields(entry: dict) -> bool:
    return bool(entry.get("id"))

def merge_data(bulk_entries: list, top_tier_entries: list) -> list:
    merged = {}
    for entry in bulk_entries:
        if not _has_required_fields(entry) or not _is_valid_url(entry.get("url")):
            continue
        merged[entry["id"]] = entry
    for entry in top_tier_entries:
        if not _has_required_fields(entry) or not _is_valid_url(entry.get("url")):
            continue
        merged[entry["id"]] = entry
    result = list(merged.values())
    result.sort(key=lambda x: x.get("date_posted", "") or "", reverse=True)
    return result

def write_json(entries: list, path: str):
    with open(path, "w") as f:
        json.dump(entries, f, indent=2)
