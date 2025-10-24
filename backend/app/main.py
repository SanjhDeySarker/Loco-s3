import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- 🔧 Fix import paths dynamically ---
# Allow imports whether running from project root or backend/
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# --- 🌐 Import routers safely ---
try:
    from backend.app.routers import buckets, objects  # if running from project root
except ModuleNotFoundError:
    from app.routers import buckets, objects          # if running from backend folder

# --- 🚀 Initialize app ---
app = FastAPI(title="Loco3 - Local S3 Alternative", version="1.0.0")

# --- 🌍 CORS (so React frontend can connect) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 🔗 Mount routers ---
app.include_router(buckets.router, prefix="/api/buckets", tags=["Buckets"])
app.include_router(objects.router, prefix="/api/objects", tags=["Objects"])

# --- 🏠 Health endpoint ---
@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "Loco3"}
