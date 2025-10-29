from fastapi import APIRouter, HTTPException
from app import crud, schemas

router = APIRouter(prefix="/api/buckets", tags=["Buckets"])

@router.get("/", response_model=list[schemas.Bucket])
def list_buckets():
    """List all buckets"""
    return crud.list_buckets()

@router.post("/", response_model=schemas.Bucket)
def create_bucket(bucket: schemas.BucketCreate):
    """Create a new bucket"""
    try:
        return crud.create_bucket(bucket.name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{bucket_name}")
def delete_bucket(bucket_name: str):
    """Delete a bucket and all its contents"""
    crud.delete_bucket(bucket_name)
    return {"message": f"Bucket '{bucket_name}' deleted successfully."}
