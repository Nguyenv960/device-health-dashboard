import json, argparse
from pathlib import Path
from uuid import UUID
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Validate a device-health snapshot.")
    parser.add_argument("snapshot_path", type = Path, help = "Path to the JSON snapshot to validate.")

    args = parser.parse_args()
    with args.snapshot_path.open("r", encoding = "utf-8-sig") as file:
        snapshot = json.load(file)

    validation_errors = validate_snapshot(snapshot)

    if validation_errors:
        print("Validation")
        for error in validation_errors:
            print(f"- {error}")
    else:
        print("Snapshot validation passed.")    

def validate_snapshot(snapshot):
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
    #Disk metric validation
    if isinstance(snapshot,dict):
        metrics = snapshot.get("metrics")
        errors = snapshot.get("errors")

        if isinstance(metrics,dict):
            disk_fields = ("disk_free_bytes", "disk_total_bytes")

            if not metrics:
                if isinstance(errors, list) and not errors:
                    validation_errors.append("Empty metrics must include a collection error.")
            else:
                for field in disk_fields:
                    if field not in metrics:
                        validation_errors.append(f"Missing required metric: {field}")
                    elif type(metrics[field]) is not int:
                        validation_errors.append(f"{field} must be an integer.")

                free = metrics.get("disk_free_bytes")
                total = metrics.get("disk_total_bytes")
                if type(free) is int and type(total) is int:
                    if total <= 0:
                        validation_errors.append("disk_total_bytes must be greater than zero.")
                    if free < 0:
                        validation_errors.append("disk_free_bytes cannot be negative.")
                    if free > total:
                        validation_errors.append("disk_free_bytes cannot exceed disk_total_bytes.")
    return validation_errors

if __name__ == "__main__":
    main()