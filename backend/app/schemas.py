from pydantic import BaseModel
from typing import Optional, List
import datetime

class BucketCreate(BaseModel):
    name: str

class BucketOut(BaseModel):
    id: int
    name: str
    created_at: datetime.datetime
    class Config:
        orm_mode = True

class ObjectOut(BaseModel):
    id: int
    key: str
    size: Optional[int]
    mime_type: Optional[str]
    created_at: datetime.datetime
    modified_at: Optional[datetime.datetime]
    class Config:
        orm_mode = True

class ObjectList(BaseModel):
    items: List[ObjectOut]
    total: int
    page: int
    per_page: int
