from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, database

router = APIRouter(prefix="/api/objects", tags=["objects"])
get_db = database.get_db

@router.post("/{bucket_name}")
async def upload_object(bucket_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    obj = crud.create_object(db, bucket_name, content, file.filename)
    if not obj:
        raise HTTPException(status_code=404, detail="Bucket not found")
    return {"key": obj.key, "bucket": bucket_name}

@router.get("/{bucket_name}")
def list_objects(bucket_name: str, db: Session = Depends(get_db)):
    return crud.get_objects(db, bucket_name)

@router.get("/{bucket_name}/{key}")
def download_object(bucket_name: str, key: str, db: Session = Depends(get_db)):
    obj = crud.get_object(db, bucket_name, key)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    from fastapi.responses import FileResponse
    return FileResponse(obj.path, filename=obj.key)

@router.delete("/{bucket_name}/{key}")
def delete_object(bucket_name: str, key: str, db: Session = Depends(get_db)):
    obj = crud.delete_object(db, bucket_name, key)
    if not obj:
        raise HTTPException(status_code=404, detail="Object not found")
    return {"detail": "Deleted"}
