from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.database import engine, Base
from app.routers import auth, artworks, collections

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MitSMK API",
    description="API for MitSMK - Art search and collection management",
    version="1.0.0",
    docs_url="/swagger",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(artworks.router, prefix="/api/artworks", tags=["Artworks"])
app.include_router(collections.router, prefix="/api/collections", tags=["Collections"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

