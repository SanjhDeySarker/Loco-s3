from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/api/buckets", tags=["buckets"])
get_db = database.get_db

@router.get("/", response_model=list[schemas.Bucket])
def list_buckets(db: Session = Depends(get_db)):
    return crud.get_buckets(db)

@router.post("/", response_model=schemas.Bucket)
def create_bucket(bucket: schemas.BucketCreate, db: Session = Depends(get_db)):
    return crud.create_bucket(db, bucket)

@router.delete("/{bucket_id}", response_model=schemas.Bucket)
def delete_bucket(bucket_id: int, db: Session = Depends(get_db)):
    bucket = crud.delete_bucket(db, bucket_id)
    if not bucket:
        raise HTTPException(status_code=404, detail="Bucket not found")
    return bucket
