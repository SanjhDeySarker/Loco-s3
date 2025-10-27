# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# -------------------------------
# Ensure 'data' directory exists
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")
os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------------
# SQLite Database URL
# -------------------------------
# Using a relative path ensures it works both locally and in production
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.abspath(os.path.join(DATA_DIR, 'storage.db'))}"

# -------------------------------
# Create SQLAlchemy Engine
# -------------------------------
# check_same_thread=False is required for SQLite when used with FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# -------------------------------
# SessionLocal for dependency injection
# -------------------------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------------------------------
# Base class for all ORM models
# -------------------------------
Base = declarative_base()


# -------------------------------
# Dependency function for FastAPI routes
# -------------------------------
def get_db():
    """
    Create a new database session for each request and close it after.
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
