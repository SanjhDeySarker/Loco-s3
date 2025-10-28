from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class Bucket(Base):
    __tablename__ = "buckets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    objects = relationship("Obj", back_populates="bucket", cascade="all, delete-orphan")

class Obj(Base):
    __tablename__ = "objects"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, nullable=False)  # object key (may include folders)
    bucket_id = Column(Integer, ForeignKey("buckets.id"), nullable=False)
    path = Column(String, nullable=False)  # filesystem path
    size = Column(Integer)
    mime_type = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    bucket = relationship("Bucket", back_populates="objects")
