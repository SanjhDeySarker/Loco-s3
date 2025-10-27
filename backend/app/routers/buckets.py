from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db

router = APIRouter()

@router.get("", response_model=list[schemas.BucketOut])
def list_buckets(db: Session = Depends(get_db)):
    return crud.list_buckets(db)

@router.post("", response_model=schemas.BucketOut)
def create_bucket(payload: schemas.BucketCreate, db: Session = Depends(get_db)):
    try:
        b = crud.create_bucket(db, payload.name)
        return b
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{bucket_name}")
def delete_bucket(bucket_name: str, db: Session = Depends(get_db)):
    ok = crud.delete_bucket(db, bucket_name)
    if not ok:
        raise HTTPException(status_code=404, detail="Bucket not found")
    return {"message": "deleted"}
