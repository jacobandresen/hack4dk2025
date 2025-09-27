from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.director import Director
from app.models.movie import Movie
from app.schemas.director import Director as DirectorSchema
from app.schemas.movie import MovieSummary
from app.services.dfi_service import DFIService
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/search", response_model=dict)
async def search_directors(
    name: str = Query(..., description="Director name to search for"),
    db: Session = Depends(get_db)
):
    """Search for directors"""
    dfi_service = DFIService()
    
    try:
        # Search in DFI API
        dfi_results = await dfi_service.search_directors(name)
        
        directors = []
        for result in dfi_results:
            # Check if director is already cached
            cached_director = db.query(Director).filter(Director.name == result.get("Name")).first()
            
            if cached_director:
                # Check if cache is still fresh (30 days)
                if cached_director.cached_at and (datetime.utcnow() - cached_director.cached_at).days < 30:
                    directors.append(DirectorSchema.from_orm(cached_director))
                    continue
            
            # Parse and cache new director data
            director_data = dfi_service.parse_director_data(result)
            db_director = Director(**director_data.dict())
            db.add(db_director)
            db.commit()
            db.refresh(db_director)
            
            directors.append(DirectorSchema.from_orm(db_director))
        
        await dfi_service.close()
        
        return {
            "directors": directors,
            "total": len(directors)
        }
        
    except Exception as e:
        await dfi_service.close()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{director_id}/movies", response_model=dict)
async def get_director_movies(director_id: int, db: Session = Depends(get_db)):
    """Get movies by director"""
    director = db.query(Director).filter(Director.id == director_id).first()
    
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    
    # Get movies by this director
    movies = db.query(Movie).filter(Movie.director == director.name).all()
    
    return {
        "director": DirectorSchema.from_orm(director),
        "movies": [MovieSummary.from_orm(movie) for movie in movies]
    }
