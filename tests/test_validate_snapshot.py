import json
from pathlib import Path

from ingest.validate_snapshot import validate_snapshot

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

def load_snapshot(filename):
    path = FIXTURES_DIR / filename

    with path.open("r", encoding = "utf-8-sig") as file:
        return json.load(file)

def test_valid_disk_snapshot_passes():
    snapshot = load_snapshot("windows_disk_ok.json")

    errors = validate_snapshot(snapshot)
    assert errors == []

def test_collection_failure_snapshot_passes_validation():
    snapshot = load_snapshot("windows_disk_volume_missing.json")

    errors = validate_snapshot(snapshot)

    assert errors == []

def test_negative_free_bytes_is_rejected():
    snapshot = load_snapshot("windows_disk_ok.json")
    snapshot["metrics"]["disk_free_bytes"] = -1

    errors = validate_snapshot(snapshot)

    assert "disk_free_bytes cannot be negative." in errors

def test_zero_total_bytes_is_rejected():
    snapshot = load_snapshot("windows_disk_ok.json")
    snapshot["metrics"]["disk_free_bytes"] = 0
    snapshot["metrics"]["disk_total_bytes"] = 0

    errors = validate_snapshot(snapshot)

    assert "disk_total_bytes must be greater than zero." in errors

def test_free_bytes_above_total_is_rejected():
    snapshot = load_snapshot("windows_disk_ok.json")
    snapshot["metrics"]["disk_free_bytes"] = (snapshot["metrics"]["disk_total_bytes"] + 1)

    errors = validate_snapshot(snapshot)

    assert "disk_free_bytes cannot exceed disk_total_bytes." in errors

def test_empty_metrics_without_error_is_rejected():
    snapshot = load_snapshot("windows_disk_ok.json")
    snapshot["metrics"] = {}
    snapshot["errors"] = []

    errors = validate_snapshot(snapshot)

    assert "Empty metrics must include a collection error." in errors
