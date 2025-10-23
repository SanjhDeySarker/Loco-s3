from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Bucket(Base):
    __tablename__ = "buckets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    objects = relationship("Object", back_populates="bucket", cascade="all, delete-orphan")

class Object(Base):
    __tablename__ = "objects"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, index=True)
    bucket_id = Column(Integer, ForeignKey("buckets.id"))
    path = Column(String)
    size = Column(Integer)
    mime_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow)

    bucket = relationship("Bucket", back_populates="objects")
