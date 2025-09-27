#!/usr/bin/env python3
"""
FastAPI-based MCP Server for SMK (Statens Museum for Kunst) API
Exposes ArtSearch and Detail resources
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class ArtworkSearchResult(BaseModel):
    """Model for artwork search results"""
    id: str
    title: str
    year: Optional[str] = None
    artist: Optional[str] = None
    image_url: Optional[str] = None


class ArtworkDetail(BaseModel):
    """Model for detailed artwork information"""
    id: str
    title: str
    year: Optional[str] = None
    artist: Optional[str] = None
    image_url: Optional[str] = None
    high_res_image_url: Optional[str] = None
    description: Optional[str] = None


class SMKAPIClient:
    """Client for interacting with SMK API"""
    
    def __init__(self):
        self.base_url = "https://api.smk.dk/api/v1"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def search_artworks(self, keys: str, offset: int = 0, rows: int = 100) -> List[ArtworkSearchResult]:
        """Search for artworks using the SMK API"""
        try:
            url = f"{self.base_url}/art/search/"
            params = {
                "keys": keys,
                "offset": offset,
                "rows": rows
            }
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            artworks = []
            
            for item in data.get("items", []):
                artwork = ArtworkSearchResult(
                    id=str(item.get("object_number", "")),
                    title=item.get("title", "Unknown Title"),
                    year=item.get("production_date", {}).get("year") if item.get("production_date") else None,
                    artist=item.get("creator", [{}])[0].get("name") if item.get("creator") else None,
                    image_url=item.get("image_url", {}).get("thumbnail") if item.get("image_url") else None
                )
                artworks.append(artwork)
            
            return artworks
            
        except httpx.HTTPError as e:
            print(f"HTTP error during search: {e}")
            return []
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    async def get_artwork_detail(self, artwork_id: str) -> Optional[ArtworkDetail]:
        """Get detailed information about a specific artwork"""
        try:
            url = f"{self.base_url}/art/object/{artwork_id}"
            
            response = await self.client.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract high resolution image URL if available
            high_res_image_url = None
            if data.get("image_url"):
                high_res_image_url = data["image_url"].get("full")
            
            artwork = ArtworkDetail(
                id=str(data.get("object_number", "")),
                title=data.get("title", "Unknown Title"),
                year=data.get("production_date", {}).get("year") if data.get("production_date") else None,
                artist=data.get("creator", [{}])[0].get("name") if data.get("creator") else None,
                image_url=data.get("image_url", {}).get("thumbnail") if data.get("image_url") else None,
                high_res_image_url=high_res_image_url,
                description=data.get("description", "")
            )
            
            return artwork
            
        except httpx.HTTPError as e:
            print(f"HTTP error during detail fetch: {e}")
            return None
        except Exception as e:
            print(f"Error during detail fetch: {e}")
            return None
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


# Initialize FastAPI app
app = FastAPI(
    title="SMK MCP Server",
    description="MCP Server for SMK (Statens Museum for Kunst) API",
    version="1.0.0"
)

# Initialize API client
api_client = SMKAPIClient()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await api_client.close()


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "SMK MCP Server",
        "description": "MCP Server for SMK (Statens Museum for Kunst) API",
        "version": "1.0.0",
        "resources": [
            {
                "name": "ArtSearch",
                "endpoint": "/search",
                "description": "Search for artworks in the SMK collection"
            },
            {
                "name": "Detail",
                "endpoint": "/detail/{artwork_id}",
                "description": "Get detailed information about a specific artwork"
            }
        ]
    }


@app.get("/search")
async def search_artworks(
    keys: str = Query(..., description="Search terms"),
    offset: int = Query(0, description="Starting position"),
    rows: int = Query(100, le=100, description="Number of results (max 100)")
):
    """Search for artworks using the SMK API"""
    if not keys.strip():
        raise HTTPException(status_code=400, detail="Keys parameter is required")
    
    artworks = await api_client.search_artworks(keys, offset, rows)
    
    return {
        "query": {
            "keys": keys,
            "offset": offset,
            "rows": rows
        },
        "results": [artwork.dict() for artwork in artworks],
        "count": len(artworks)
    }


@app.get("/detail/{artwork_id}")
async def get_artwork_detail(artwork_id: str):
    """Get detailed information about a specific artwork"""
    artwork = await api_client.get_artwork_detail(artwork_id)
    
    if not artwork:
        raise HTTPException(status_code=404, detail="Artwork not found")
    
    return artwork.dict()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "SMK MCP Server"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

