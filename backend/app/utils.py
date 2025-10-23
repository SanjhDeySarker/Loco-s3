import os
from pathlib import Path

STORAGE_PATH = "storage"

def safe_path(bucket_name: str, key: str) -> str:
    """
    Ensure no path traversal: joins bucket_name and key safely.
    """
    bucket_path = Path(STORAGE_PATH) / bucket_name
    full_path = bucket_path / key
    if not full_path.resolve().is_relative_to(bucket_path.resolve()):
        raise ValueError("Invalid key: path traversal detected")
    return str(full_path)

def ensure_bucket_dir(bucket_name: str):
    path = Path(STORAGE_PATH) / bucket_name
    path.mkdir(parents=True, exist_ok=True)
