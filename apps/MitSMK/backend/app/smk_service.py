import httpx
import os
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from .models import Artwork
from .schemas import Artwork as ArtworkSchema

SMK_API_BASE_URL = os.getenv("SMK_API_BASE_URL", "https://api.smk.dk/api/v1")

class SMKService:
    def __init__(self):
        self.base_url = SMK_API_BASE_URL

    async def search_artworks(self, query: str, offset: int = 0, limit: int = 20) -> Dict[str, Any]:
        """Search for artworks using SMK API"""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/art/search/"
            params = {
                "keys": query,
                "offset": offset,
                "rows": limit,
                "filters": "[has_image:true]"  # Only artworks with images
            }
            
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def get_artwork_details(self, object_number: str) -> Dict[str, Any]:
        """Get detailed information about a specific artwork"""
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/art/"
            params = {"object_number": object_number}
            
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    def parse_artwork_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse SMK API data into our artwork format"""
        # Extract title
        title = None
        if "titles" in data and data["titles"]:
            title = data["titles"][0].get("title")
        
        # Extract year
        year = None
        if "production_dates" in data and data["production_dates"]:
            year = data["production_dates"][0].get("year")
        
        # Extract artist name
        artist_name = None
        if "production" in data and data["production"] and len(data["production"]) > 0:
            # Get creator name from production array
            production = data["production"][0]
            if "creator" in production and production["creator"]:
                artist_name = production["creator"]
        elif "creators" in data and data["creators"]:
            # Fallback to creators array if production doesn't have creator
            artist_name = data["creators"][0].get("name")
        
        # Extract image information
        image_thumbnail = data.get("image_thumbnail")
        image_iiif_id = data.get("image_iiif_id")
        
        # Extract other properties
        public_domain = data.get("public_domain", False)
        object_names = []
        if "object_names" in data and data["object_names"]:
            for item in data["object_names"]:
                if isinstance(item, dict) and "name" in item:
                    object_names.append(item["name"])
                elif isinstance(item, str):
                    object_names.append(item)
        has_image = data.get("has_image", False)
        
        return {
            "object_number": data.get("object_number", ""),
            "title": title,
            "year": year,
            "artist_name": artist_name,
            "image_thumbnail": image_thumbnail,
            "image_iiif_id": image_iiif_id,
            "public_domain": public_domain,
            "object_names": object_names,
            "has_image": has_image,
            "raw_data": data
        }

    async def search_and_cache_artworks(
        self, 
        query: str, 
        offset: int = 0, 
        limit: int = 20, 
        db: Session = None
    ) -> List[ArtworkSchema]:
        """Search artworks and cache them in database"""
        # Search SMK API
        search_result = await self.search_artworks(query, offset, limit)
        
        artworks = []
        if "items" in search_result:
            for item_data in search_result["items"]:
                # Parse artwork data
                artwork_data = self.parse_artwork_data(item_data)
                
                # Check if artwork already exists in cache
                existing_artwork = db.query(Artwork).filter(
                    Artwork.object_number == artwork_data["object_number"]
                ).first()
                
                if existing_artwork:
                    artworks.append(ArtworkSchema.from_orm(existing_artwork))
                else:
                    # Create new artwork in database
                    new_artwork = Artwork(**artwork_data)
                    db.add(new_artwork)
                    db.commit()
                    db.refresh(new_artwork)
                    artworks.append(ArtworkSchema.from_orm(new_artwork))
        
        return artworks

    async def get_artwork_by_object_number(
        self, 
        object_number: str, 
        db: Session = None
    ) -> Optional[ArtworkSchema]:
        """Get artwork by object number, fetching from SMK API if not cached"""
        # Check if artwork exists in cache
        existing_artwork = db.query(Artwork).filter(
            Artwork.object_number == object_number
        ).first()
        
        if existing_artwork:
            return ArtworkSchema.from_orm(existing_artwork)
        
        # Fetch from SMK API
        try:
            artwork_data = await self.get_artwork_details(object_number)
            parsed_data = self.parse_artwork_data(artwork_data)
            
            # Cache in database
            new_artwork = Artwork(**parsed_data)
            db.add(new_artwork)
            db.commit()
            db.refresh(new_artwork)
            
            return ArtworkSchema.from_orm(new_artwork)
        except Exception:
            return None
