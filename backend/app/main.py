from fastapi import FastAPI
from .database import engine, Base
from .routers import buckets, objects
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Loco3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(buckets.router)
app.include_router(objects.router)
