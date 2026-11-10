import shutil
from pathlib import Path

target_path = Path.home()
disk = shutil.disk_usage(target_path)

print(f"Measured path: {target_path}")
print(f"Total bytes: {disk.total}")
print(f"Used bytes: {disk.used}")
print(f"Free bytes: {disk.free}")
free_percent = (disk.free / disk.total) * 100
print(f"Free space: {free_percent:.2f}%")

snapshot = {
    "disk_total_bytes": disk.total,
    "disk_used_bytes": disk.used,
    "disk_free_bytes": disk.free,
    "disk_free_percent": free_percent,
}
print(snapshot)