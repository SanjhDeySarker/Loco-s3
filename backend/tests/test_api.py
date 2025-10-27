import asyncio
import os
import tempfile
import shutil
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import models
from app.database import engine, SessionLocal

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_env(tmp_path):
    # Use tmp storage and tmp sqlite for tests
    storage = tmp_path / "storage"
    data = tmp_path / "data"
    storage.mkdir()
    data.mkdir()
    # patch settings environment variables by setting env vars (app.config loads from .env earlier
    os.environ["STORAGE_PATH"] = str(storage)
    os.environ["DATABASE_URL"] = f"sqlite:///{data / 'test.db'}"
    # Recreate DB tables in the test DB file
    # This is a simple approach; because models.Base.metadata was created at import time,
    # we rebind the engine by creating tables directly
    from app import database, models as m
    engine_test = create_engine(os.environ["DATABASE_URL"], connect_args={"check_same_thread": False})
    m.Base.metadata.create_all(bind=engine_test)
    yield
    # cleanup implicit by tmp_path

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"

def test_bucket_create_list_delete():
    # create
    r = client.post("/api/buckets", json={"name": "my-bucket"})
    assert r.status_code == 200
    assert r.json()["name"] == "my-bucket"
    # list
    r = client.get("/api/buckets")
    assert r.status_code == 200
    arr = r.json()
    assert any(b["name"] == "my-bucket" for b in arr)
    # delete
    r = client.delete("/api/buckets/my-bucket")
    assert r.status_code == 200
    r = client.get("/api/buckets")
    assert all(b["name"] != "my-bucket" for b in r.json())

def test_upload_download_delete_object():
    # create bucket
    client.post("/api/buckets", json={"name": "b"})
    # upload
    file_content = b"hello world"
    r = client.put("/api/b/b.txt", files={"file": ("b.txt", file_content, "text/plain")})
    assert r.status_code == 200
    # list objects
    r = client.get("/api/b")
    assert r.status_code == 200
    assert r.json()["total"] == 1
    # download
    r = client.get("/api/b/b.txt")
    assert r.status_code == 200
    assert r.content == file_content
    # delete
    r = client.delete("/api/b/b.txt")
    assert r.status_code == 200
    r = client.get("/api/b")
    assert r.json()["total"] == 0
