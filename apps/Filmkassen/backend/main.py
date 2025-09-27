from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api import auth, movies, directors, collections
from app.core.config import settings
from app.core.database import engine
from app.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Filmkassen API",
    description="API for film search and collection management using DFI's API",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(directors.router, prefix="/directors", tags=["Directors"])
app.include_router(collections.router, prefix="/collections", tags=["Collections"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Filmkassen API", "version": "1.0.0"}
