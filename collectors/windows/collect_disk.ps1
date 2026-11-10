$fmt = "yyyy-MM-dd'T'HH:mm:ss'Z'"
$started = (Get-Date).ToUniversalTime()
$errors = @()
$checks = @()
try {
    $vol = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'" -ErrorAction Stop
    if (-not $vol) { throw "Volume C: not found" }
    $metrics = @{ disk_free_bytes = [int64]$vol.FreeSpace; disk_total_bytes = [int64]$vol.Size }
} catch {
    $errors += $_.Exception.Message
    $metrics = @{}
}
$out = [ordered]@{
    schema_version = "1.0"
    collector_version = "0.1.0"
    device_id = "ab646e3c-c5cb-476d-84f2-552a081af335"
    run_id = [guid]::NewGuid().ToString()
    collection_started_at_utc = $started.ToString($fmt)
    collection_finished_at_utc = (Get-Date).ToUniversalTime().ToString($fmt)
    metrics = $metrics
    checks = $checks
    errors = @($errors)
}
$out | ConvertTo-Json -Depth 5