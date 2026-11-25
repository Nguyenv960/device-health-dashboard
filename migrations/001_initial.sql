CREATE TABLE IF NOT EXISTS devices (
    device_id TEXT NOT NULL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS collection_runs (
    run_id TEXT NOT NULL PRIMARY KEY,
    device_id TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    collector_verison TEXT NOT NULL,
    collection_started_at_utc TEXT NOT NULL,
    collector_finished_at_utc TEXT NOT NULL,
    received_at_utc TEXT NOT NULL,
    errors_json TEXT NOT NULL,

    FOREIGN KEY (device_id) REFERENCES devices(device_id)
);

CREATE TABLE IF NOT EXISTS disk_samples (
    run_id TEXT NOT NULL PRIMARY KEY,
    disk_free_bytes INTEGER NOT NULL,
    disk_total_bytes INTEGER NOT NULL,

    FOREIGN KEY (run_id) REFERENCES collection_run(run_id)
);

CREATE INDEX IF NOT EXISTS idx_collection_runs_device_started 
ON collection_runs (device_id,collection_started_at_utc);
