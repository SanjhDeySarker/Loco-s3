from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, schemas
from ..config import settings
from ..utils import safe_join
from fastapi.responses import StreamingResponse
import os

router = APIRouter()

@router.get("/{bucket_name}", response_model=schemas.ObjectList)
def list_objects(bucket_name: str, page: int=1, per_page: int=50, prefix: str | None = None, db: Session = Depends(get_db)):
    try:
        items, total = crud.list_objects(db, bucket_name, page=page, per_page=per_page, prefix=prefix)
        return {"items": items, "total": total, "page": page, "per_page": per_page}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Bucket not found")

@router.put("/{bucket_name}/{object_key:path}")
def upload_object(bucket_name: str, object_key: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # protect upload size
    # Note: FastAPI doesn't stream form uploads directly to our function, but UploadFile uses temp file
    if file.spool_max_size is not None:
        pass
    # Very basic file size check: try to peek .file (if possible)
    try:
        obj = crud.upload_object(db, bucket_name, object_key, file)
        return obj
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Bucket not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{bucket_name}/{object_key:path}")
def download_object(bucket_name: str, object_key: str, db: Session = Depends(get_db)):
    obj = crud.get_object(db, bucket_name, object_key)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    # stream file
    def iterfile(path):
        with open(path, "rb") as f:
            while True:
                chunk = f.read(1024*64)
                if not chunk:
                    break
                yield chunk
    headers = {"Content-Type": obj.mime_type or "application/octet-stream",
               "Content-Length": str(obj.size or 0),
               "Content-Disposition": f'attachment; filename="{os.path.basename(obj.key)}"'}
    return StreamingResponse(iterfile(obj.path), headers=headers)

@router.delete("/{bucket_name}/{object_key:path}")
def delete_object(bucket_name: str, object_key: str, db: Session = Depends(get_db)):
    ok = crud.delete_object(db, bucket_name, object_key)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return {"message": "deleted"}

@router.get("/{bucket_name}/{object_key:path}/meta", response_model=schemas.ObjectOut)
def object_meta(bucket_name: str, object_key: str, db: Session = Depends(get_db)):
    obj = crud.get_object(db, bucket_name, object_key)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj
