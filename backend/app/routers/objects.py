from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app import crud

router = APIRouter(prefix="/api", tags=["Objects"])

@router.get("/{bucket_name}")
def list_objects(bucket_name: str):
    """List all objects in a bucket"""
    return crud.list_objects(bucket_name)

@router.get("/{bucket_name}/{object_key:path}")
def get_object(bucket_name: str, object_key: str):
    """Download an object"""
    file_path = crud.get_object_path(bucket_name, object_key)
    if not file_path:
        raise HTTPException(status_code=404, detail="Object not found")
    return FileResponse(file_path)

@router.put("/{bucket_name}/{object_key:path}")
async def upload_object(bucket_name: str, object_key: str, file: UploadFile = File(...)):
    """Upload or replace an object"""
    try:
        return crud.upload_object(bucket_name, object_key, file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{bucket_name}/{object_key:path}")
def delete_object(bucket_name: str, object_key: str):
    """Delete an object"""
    crud.delete_object(bucket_name, object_key)
    return {"message": f"Object '{object_key}' deleted from bucket '{bucket_name}'."}
