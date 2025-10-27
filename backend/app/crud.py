import os
from sqlalchemy.orm import Session
from . import models
from .config import settings
from .utils import safe_join, atomic_save, detect_mime
import datetime

# Bucket operations
def create_bucket(db: Session, name: str):
    name = name.strip()
    if not name:
        raise ValueError("Bucket name required")
    # basic allowed characters check
    import re
    if not re.match(r"^[a-z0-9._-]+$", name):
        raise ValueError("Invalid bucket name (use a-z0-9 . _ - )")
    existing = db.query(models.Bucket).filter(models.Bucket.name == name).first()
    if existing:
        raise ValueError("Bucket already exists")
    b = models.Bucket(name=name)
    db.add(b)
    db.commit()
    db.refresh(b)
    # create directory
    path = safe_join(settings.STORAGE_PATH, name)
    os.makedirs(path, exist_ok=True)
    return b

def list_buckets(db: Session):
    return db.query(models.Bucket).order_by(models.Bucket.created_at.desc()).all()

def delete_bucket(db: Session, name: str):
    b = db.query(models.Bucket).filter(models.Bucket.name == name).first()
    if not b:
        return False
    # remove files from storage
    path = safe_join(settings.STORAGE_PATH, name)
    if os.path.exists(path):
        import shutil
        shutil.rmtree(path)
    db.delete(b)
    db.commit()
    return True

# Object operations
def list_objects(db: Session, bucket_name: str, page: int=1, per_page:int=50, prefix: str=None):
    b = db.query(models.Bucket).filter(models.Bucket.name == bucket_name).first()
    if not b:
        raise FileNotFoundError("Bucket not found")
    q = db.query(models.Obj).filter(models.Obj.bucket_id == b.id)
    if prefix:
        q = q.filter(models.Obj.key.like(f"{prefix}%"))
    total = q.count()
    items = q.order_by(models.Obj.created_at.desc()).offset((page-1)*per_page).limit(per_page).all()
    return items, total

def get_object(db: Session, bucket_name: str, object_key: str):
    b = db.query(models.Bucket).filter(models.Bucket.name == bucket_name).first()
    if not b:
        return None
    obj = db.query(models.Obj).filter(models.Obj.bucket_id==b.id, models.Obj.key==object_key).first()
    return obj

def upload_object(db: Session, bucket_name: str, object_key: str, upload_file):
    # bucket must exist
    b = db.query(models.Bucket).filter(models.Bucket.name == bucket_name).first()
    if not b:
        raise FileNotFoundError("Bucket not found")
    # ensure safe path
    bucket_path = safe_join(settings.STORAGE_PATH, bucket_name)
    dest_path = safe_join(bucket_path, object_key)
    # stream-save atomic
    # upload_file is FastAPI UploadFile: use .file (a SpooledTemporaryFile)
    # We'll handle both file-like and starndard objects.
    file_like = upload_file.file if hasattr(upload_file, "file") else upload_file
    atomic_save(file_like, dest_path)
    size = os.path.getsize(dest_path)
    mime = detect_mime(dest_path)
    # upsert DB object
    existing = db.query(models.Obj).filter(models.Obj.bucket_id==b.id, models.Obj.key==object_key).first()
    if existing:
        existing.path = dest_path
        existing.size = size
        existing.mime_type = mime
        existing.modified_at = datetime.datetime.utcnow()
        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        obj = models.Obj(
            key=object_key,
            bucket_id=b.id,
            path=dest_path,
            size=size,
            mime_type=mime
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

def delete_object(db: Session, bucket_name: str, object_key: str):
    obj = get_object(db, bucket_name, object_key)
    if not obj:
        return False
    if os.path.exists(obj.path):
        try:
            os.remove(obj.path)
        except Exception:
            pass
    db.delete(obj)
    db.commit()
    return True
