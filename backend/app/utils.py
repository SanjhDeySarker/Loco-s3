import os
import tempfile
import shutil
import magic
from .config import settings

def safe_join(base: str, *paths: str) -> str:
    """
    Join base and paths and ensure resulting path is inside base.
    Raises ValueError if path traversal detected.
    """
    base = os.path.abspath(base)
    joined = os.path.abspath(os.path.join(base, *paths))
    if not joined.startswith(base + os.sep) and joined != base:
        raise ValueError("Unsafe path detected")
    return joined

def atomic_save(stream, dest_path: str, chunk_size: int = 1024*1024):
    """
    Save an async-like stream or fileobj to dest_path atomically.
    'stream' should be a file-like object with read() method or an UploadFile from FastAPI.
    We'll accept objects with .read() that may be async — but for simplicity we call .read() synchronously here.
    """
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=dest_dir)
    os.close(fd)
    try:
        with open(tmp, "wb") as f:
            # stream might be FastAPI UploadFile (has read). We'll loop.
            while True:
                chunk = stream.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
        # atomic replace
        os.replace(tmp, dest_path)
    except Exception:
        try:
            os.remove(tmp)
        except Exception:
            pass
        raise

def detect_mime(path: str) -> str:
    try:
        m = magic.Magic(mime=True)
        return m.from_file(path)
    except Exception:
        # fallback
        return "application/octet-stream"
