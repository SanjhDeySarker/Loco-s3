import os
from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime

STORAGE_PATH = "storage"

# Bucket CRUD
def create_bucket(db: Session, bucket: schemas.BucketCreate):
    db_bucket = models.Bucket(name=bucket.name)
    db.add(db_bucket)
    db.commit()
    db.refresh(db_bucket)
    os.makedirs(os.path.join(STORAGE_PATH, bucket.name), exist_ok=True)
    return db_bucket

def get_buckets(db: Session):
    return db.query(models.Bucket).all()

def get_bucket(db: Session, bucket_id: int):
    return db.query(models.Bucket).filter(models.Bucket.id == bucket_id).first()

def delete_bucket(db: Session, bucket_id: int):
    bucket = get_bucket(db, bucket_id)
    if bucket:
        path = os.path.join(STORAGE_PATH, bucket.name)
        if os.path.exists(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(path)
        db.delete(bucket)
        db.commit()
    return bucket

# Object CRUD
def create_object(db: Session, bucket_name: str, file, key: str):
    bucket = db.query(models.Bucket).filter(models.Bucket.name==bucket_name).first()
    if not bucket:
        return None
    file_path = os.path.join(STORAGE_PATH, bucket_name, key)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(file)
    db_object = models.Object(
        key=key,
        bucket_id=bucket.id,
        path=file_path,
        size=len(file),
        mime_type="application/octet-stream",
        created_at=datetime.utcnow(),
        modified_at=datetime.utcnow()
    )
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object

def get_objects(db: Session, bucket_name: str):
    bucket = db.query(models.Bucket).filter(models.Bucket.name==bucket_name).first()
    if not bucket:
        return []
    return db.query(models.Object).filter(models.Object.bucket_id==bucket.id).all()

def get_object(db: Session, bucket_name: str, key: str):
    bucket = db.query(models.Bucket).filter(models.Bucket.name==bucket_name).first()
    if not bucket:
        return None
    return db.query(models.Object).filter(models.Object.bucket_id==bucket.id, models.Object.key==key).first()

def delete_object(db: Session, bucket_name: str, key: str):
    obj = get_object(db, bucket_name, key)
    if obj:
        if os.path.exists(obj.path):
            os.remove(obj.path)
        db.delete(obj)
        db.commit()
    return obj
