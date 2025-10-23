from pydantic import BaseModel
from datetime import datetime

class BucketBase(BaseModel):
    name: str

class BucketCreate(BucketBase):
    pass

class Bucket(BucketBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class ObjectBase(BaseModel):
    key: str

class ObjectCreate(ObjectBase):
    pass

class Object(ObjectBase):
    id: int
    bucket_id: int
    size: int
    mime_type: str
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True
