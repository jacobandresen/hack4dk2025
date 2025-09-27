import httpx
from typing import List, Optional, Dict, Any
from app.core.config import settings
from app.schemas.movie import MovieCreate
from app.schemas.director import DirectorCreate
import os

class DFIService:
    def __init__(self):
        self.base_url = settings.DFI_API_BASE_URL
        self.username = os.getenv("DFI_API_USERNAME", "hack4dk")
        self.password = os.getenv("DFI_API_PASSWORD", "qWSzXlO5I9Wdef_NKcOJ")
        self.client = httpx.AsyncClient(
            timeout=30.0,
            auth=(self.username, self.password)
        )

    async def search_movies(self, title: str) -> List[Dict[str, Any]]:
        """Search for movies by title"""
        try:
            response = await self.client.get(
                f"{self.base_url}/film",
                params={"Title": title}
            )
            response.raise_for_status()
            data = response.json()
            # Handle DFI API response format
            if isinstance(data, dict) and "FilmList" in data:
                movies = data["FilmList"]
            elif isinstance(data, list):
                movies = data
            elif isinstance(data, dict):
                movies = data.get("results", data.get("data", []))
            else:
                return []
            
            # For each movie, get detailed information to include poster and director data
            detailed_movies = []
            for movie in movies[:10]:  # Limit to first 10 movies for performance
                if "Id" in movie:
                    detailed_movie = await self.get_movie_details(movie["Id"])
                    if detailed_movie:
                        detailed_movies.append(detailed_movie)
                    else:
                        detailed_movies.append(movie)  # Fallback to basic data
                else:
                    detailed_movies.append(movie)
            
            return detailed_movies
        except httpx.HTTPError as e:
            print(f"Error searching movies: {e}")
            return []

    async def get_movie_details(self, dfi_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed information about a movie"""
        try:
            response = await self.client.get(f"{self.base_url}/film/{dfi_id}")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Error getting movie details: {e}")
            return None

    async def search_directors(self, name: str) -> List[Dict[str, Any]]:
        """Search for directors by name"""
        try:
            response = await self.client.get(
                f"{self.base_url}/person",
                params={"Name": name}
            )
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except httpx.HTTPError as e:
            print(f"Error searching directors: {e}")
            return []

    def parse_movie_data(self, data: Dict[str, Any]) -> MovieCreate:
        """Parse DFI API movie data into our schema"""
        # Extract poster URL from the first available poster
        poster_url = None
        if "Posters" in data and data["Posters"]:
            # Use the first poster's medium-sized image
            first_poster = data["Posters"][0]
            if "ScaledCropped" in first_poster:
                for crop in first_poster["ScaledCropped"]:
                    if crop["Name"] == "landscape43M":  # Medium landscape format
                        poster_url = crop["Path"]
                        break
                # Fallback to mini if medium not available
                if not poster_url:
                    for crop in first_poster["ScaledCropped"]:
                        if crop["Name"] == "landscape43S":  # Small landscape format
                            poster_url = crop["Path"]
                            break
        
        # Extract director from person credits data
        director = None
        if "PersonCredits" in data:
            for person in data["PersonCredits"]:
                if person.get("Type") == "Instruktion" and person.get("TypeCode") == "instr":
                    director = person.get("Name")
                    break
        
        return MovieCreate(
            dfi_id=data.get("Id", 0),
            title=data.get("Title", ""),
            year=data.get("ReleaseYear"),
            poster_url=poster_url,
            director=director,
            cast=data.get("Cast", []),
            clips=data.get("Clips", []),
            videotek_url=data.get("VideotekUrl"),
            description=data.get("Description")
        )

    def parse_director_data(self, data: Dict[str, Any]) -> DirectorCreate:
        """Parse DFI API director data into our schema"""
        return DirectorCreate(
            name=data.get("Name", ""),
            dfi_id=str(data.get("Id", "")),
            bio=data.get("Bio")
        )

    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
