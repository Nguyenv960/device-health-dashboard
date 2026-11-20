import json
from pathlib import Path
from uuid import UUID
from datetime import datetime

repo_root = Path(__file__).resolve().parent.parent
fixture_path = repo_root / "tests" / "fixtures" / "windows_disk_ok.json"

with fixture_path.open("r", encoding = "utf-8-sig") as file:
    snapshot = json.load(file)

expected_types = {
    "schema_version": str,
    "collector_version": str,
    "device_id": str,
    "run_id": str,
    "collection_started_at_utc": str,
    "collection_finished_at_utc": str,
    "metrics": dict,
    "checks": list,
    "errors": list,
}
validation_errors = []

if not isinstance(snapshot, dict):
    validation_errors.append("Snapshot must be a JSON object")
else:
    for field, expected_type in expected_types.items():
        if field not in snapshot:
            validation_errors.append(f"Missing required field: {field}")
        elif not isinstance(snapshot[field], expected_type):
            actual_type = type(snapshot[field]).__name__
            validation_errors.append(f"{field} must be {expected_type.__name__}, got {actual_type}")

#uuid validation
if isinstance(snapshot, dict):
    for field in ("device_id", "run_id"):
        value = snapshot.get(field)
        if isinstance(value, str):
            try:
                UUID(value)
            except ValueError:
                validation_errors.append(f"{field} must contain a valid UUID.")

#timestap validation
parsed_times = {}

if isinstance(snapshot, dict):
    for field in ("collection_started_at_utc", "collection_finished_at_utc",):
        value = snapshot.get(field)

        if isinstance(value, str):
            if not value.endswith("Z"):
                validation_errors.append(f"{field} must end with Z to indicate UTC.")
                continue
            try:
                parsed_times[field] = datetime.fromisoformat(value)
            except ValueError:
                validation_errors.append(f"{field} must contain a valid ISO 8601 timestamp.")
    if len(parsed_times) == 2:
        started = parsed_times["collection_started_at_utc"]
        finished = parsed_times["collection_finished_at_utc"]

        if finished < started:
            validation_errors.append(
                "Collection finish time must not precede start time."
            )

if validation_errors:
    print("Validation failed:")
    for error in validation_errors:
        print(f"- {error}")
else:
    print("Snapshot validation passed.")