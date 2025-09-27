#!/usr/bin/env python3
"""
MCP Server for SMK (Statens Museum for Kunst) API
Exposes ArtSearch and Detail resources
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
import httpx
from mcp.server import Server
from mcp.server.models import Resource
from mcp.server.stdio import stdio_server
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


# Initialize the MCP server
server = Server("smk-mcp-server")
api_client = SMKAPIClient()


@server.list_resources()
async def list_resources() -> List[Resource]:
    """List available resources"""
    return [
        Resource(
            uri="smk://artsearch",
            name="ArtSearch",
            description="Search for artworks in the SMK collection",
            mimeType="application/json"
        ),
        Resource(
            uri="smk://detail",
            name="Detail",
            description="Get detailed information about a specific artwork",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a resource by URI"""
    if uri == "smk://artsearch":
        # Return search interface information
        return json.dumps({
            "type": "search_interface",
            "description": "Search for artworks using the 'keys' parameter",
            "example": "smk://artsearch?keys=amager&offset=0&rows=100",
            "parameters": {
                "keys": "Search terms (required)",
                "offset": "Starting position (default: 0)",
                "rows": "Number of results (default: 100, max: 100)"
            }
        })
    
    elif uri == "smk://detail":
        # Return detail interface information
        return json.dumps({
            "type": "detail_interface",
            "description": "Get detailed information about a specific artwork",
            "example": "smk://detail?id=KMS1234",
            "parameters": {
                "id": "Artwork ID (required)"
            }
        })
    
    elif uri.startswith("smk://artsearch?"):
        # Handle search requests
        from urllib.parse import parse_qs, urlparse
        parsed = urlparse(uri)
        params = parse_qs(parsed.query)
        
        keys = params.get("keys", [""])[0]
        offset = int(params.get("offset", ["0"])[0])
        rows = min(int(params.get("rows", ["100"])[0]), 100)
        
        if not keys:
            return json.dumps({"error": "Keys parameter is required"})
        
        artworks = await api_client.search_artworks(keys, offset, rows)
        return json.dumps([artwork.dict() for artwork in artworks])
    
    elif uri.startswith("smk://detail?"):
        # Handle detail requests
        from urllib.parse import parse_qs, urlparse
        parsed = urlparse(uri)
        params = parse_qs(parsed.query)
        
        artwork_id = params.get("id", [""])[0]
        
        if not artwork_id:
            return json.dumps({"error": "ID parameter is required"})
        
        artwork = await api_client.get_artwork_detail(artwork_id)
        if artwork:
            return json.dumps(artwork.dict())
        else:
            return json.dumps({"error": "Artwork not found"})
    
    else:
        return json.dumps({"error": "Unknown resource"})


async def main():
    """Main entry point"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

