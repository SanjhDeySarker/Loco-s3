from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import buckets, objects

# ----------------------------
# 🚀 Initialize FastAPI app
app = FastAPI(
    title="Loco3 - Self-Hosted S3 Alternative",
    version="1.0.0",
    description="Local file storage system using FastAPI + SQLite"
)

# ----------------------------
# 🌍 CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# 🔗 Include routers
app.include_router(buckets.router, prefix="/api/buckets", tags=["Buckets"])
app.include_router(objects.router, prefix="/api/objects", tags=["Objects"])

# ----------------------------
# 🏠 Health check endpoint
@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "Loco3"}
