#!/usr/bin/env python3
"""
Simple MCP Server for SMK (Statens Museum for Kunst) API
Compatible with Python 3.9
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
import httpx
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
                # Extract title from titles array
                title = "Unknown Title"
                if item.get("titles") and len(item.get("titles", [])) > 0:
                    title = item.get("titles", [{}])[0].get("title", "Unknown Title")
                
                # Extract year from production_date
                year = None
                if item.get("production_date") and len(item.get("production_date", [])) > 0:
                    year = item.get("production_date", [{}])[0].get("year")
                
                artwork = ArtworkSearchResult(
                    id=str(item.get("object_number", "")),
                    title=title,
                    year=year,
                    artist=item.get("artist", [None])[0] if item.get("artist") and len(item.get("artist", [])) > 0 else None,
                    image_url=item.get("image_thumbnail")
                )
                artworks.append(artwork)
            
            return artworks
            
        except httpx.HTTPError as e:
            print(f"HTTP error during search: {e}", file=sys.stderr)
            return []
        except Exception as e:
            print(f"Error during search: {e}", file=sys.stderr)
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
                artist=data.get("creator", [{}])[0].get("name") if data.get("creator") and len(data.get("creator", [])) > 0 else None,
                image_url=data.get("image_url", {}).get("thumbnail") if data.get("image_url") else None,
                high_res_image_url=high_res_image_url,
                description=data.get("description", "")
            )
            
            return artwork
            
        except httpx.HTTPError as e:
            print(f"HTTP error during detail fetch: {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Error during detail fetch: {e}", file=sys.stderr)
            return None
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


async def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """Handle MCP-style requests"""
    method = request.get("method")
    params = request.get("params", {})
    request_id = request.get("id")
    
    api_client = SMKAPIClient()
    
    try:
        if method == "resources/list":
            # List available resources
            resources = [
                {
                    "uri": "smk://artsearch",
                    "name": "ArtSearch",
                    "description": "Search for artworks in the SMK collection",
                    "mimeType": "application/json"
                },
                {
                    "uri": "smk://detail",
                    "name": "Detail", 
                    "description": "Get detailed information about a specific artwork",
                    "mimeType": "application/json"
                }
            ]
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {"resources": resources}
            }
        
        elif method == "resources/read":
            uri = params.get("uri", "")
            
            if uri == "smk://artsearch":
                # Return search interface information
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "contents": [{
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": json.dumps({
                                "type": "search_interface",
                                "description": "Search for artworks using the 'keys' parameter",
                                "example": "smk://artsearch?keys=amager&offset=0&rows=100",
                                "parameters": {
                                    "keys": "Search terms (required)",
                                    "offset": "Starting position (default: 0)",
                                    "rows": "Number of results (default: 100, max: 100)"
                                }
                            })
                        }]
                    }
                }
            
            elif uri == "smk://detail":
                # Return detail interface information
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "contents": [{
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": json.dumps({
                                "type": "detail_interface",
                                "description": "Get detailed information about a specific artwork",
                                "example": "smk://detail?id=KMS1234",
                                "parameters": {
                                    "id": "Artwork ID (required)"
                                }
                            })
                        }]
                    }
                }
            
            elif uri.startswith("smk://artsearch?"):
                # Handle search requests
                from urllib.parse import parse_qs, urlparse
                parsed = urlparse(uri)
                query_params = parse_qs(parsed.query)
                
                keys = query_params.get("keys", [""])[0]
                offset = int(query_params.get("offset", ["0"])[0])
                rows = min(int(query_params.get("rows", ["100"])[0]), 100)
                
                if not keys:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32602, "message": "Keys parameter is required"}
                    }
                
                artworks = await api_client.search_artworks(keys, offset, rows)
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "contents": [{
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": json.dumps([artwork.model_dump() for artwork in artworks])
                        }]
                    }
                }
            
            elif uri.startswith("smk://detail?"):
                # Handle detail requests
                from urllib.parse import parse_qs, urlparse
                parsed = urlparse(uri)
                query_params = parse_qs(parsed.query)
                
                artwork_id = query_params.get("id", [""])[0]
                
                if not artwork_id:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32602, "message": "ID parameter is required"}
                    }
                
                artwork = await api_client.get_artwork_detail(artwork_id)
                if artwork:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "contents": [{
                                "uri": uri,
                                "mimeType": "application/json",
                                "text": json.dumps(artwork.model_dump())
                            }]
                        }
                    }
                else:
                    return {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {"code": -32602, "message": "Artwork not found"}
                    }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {"code": -32601, "message": "Unknown resource"}
                }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": "Method not found"}
            }
    
    finally:
        await api_client.close()


async def main():
    """Main entry point for stdio communication"""
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            try:
                request = json.loads(line)
                response = await handle_request(request)
                print(json.dumps(response))
                sys.stdout.flush()
            except json.JSONDecodeError:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"}
                }
                print(json.dumps(error_response))
                sys.stdout.flush()
        
        except Exception as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }
            print(json.dumps(error_response))
            sys.stdout.flush()


if __name__ == "__main__":
    asyncio.run(main())