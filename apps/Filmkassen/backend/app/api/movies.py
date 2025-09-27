from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.movie import Movie
from app.schemas.movie import MovieSummary, Movie as MovieSchema
from app.services.dfi_service import DFIService
from datetime import datetime, timedelta, timezone

router = APIRouter()

@router.get("/search", response_model=dict)
async def search_movies(
    title: str = Query(..., description="Movie title to search for"),
    director: Optional[str] = Query(None, description="Director name to search for"),
    db: Session = Depends(get_db)
):
    """Search for movies"""
    dfi_service = DFIService()
    
    try:
        # Search in DFI API
        dfi_results = await dfi_service.search_movies(title)
        print(f"DFI API returned {len(dfi_results)} results")
        
        movies = []
        for i, result in enumerate(dfi_results):
            try:
                # Check if movie is already cached
                cached_movie = db.query(Movie).filter(Movie.dfi_id == result.get("Id")).first()
                
                if cached_movie:
                    # Check if cache is still fresh (7 days)
                    if cached_movie.cached_at and (datetime.now(timezone.utc) - cached_movie.cached_at).days < 7:
                        movies.append(MovieSummary.model_validate(cached_movie))
                        continue
                
                # Parse and cache new movie data
                movie_data = dfi_service.parse_movie_data(result)
                db_movie = Movie(**movie_data.model_dump())
                db.add(db_movie)
                db.commit()
                db.refresh(db_movie)
                
                movies.append(MovieSummary.model_validate(db_movie))
                print(f"Processed movie {i+1}: {db_movie.title}")
                
            except Exception as e:
                print(f"Error processing movie {i+1}: {e}")
                continue
        
        await dfi_service.close()
        
        return {
            "movies": movies,
            "total": len(movies)
        }
        
    except Exception as e:
        print(f"Search error: {e}")
        await dfi_service.close()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{movie_id}", response_model=MovieSchema)
async def get_movie_details(movie_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a movie"""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Check if cache is fresh, if not refresh from DFI API
    if not movie.cached_at or (datetime.now(timezone.utc) - movie.cached_at).days >= 7:
        dfi_service = DFIService()
        try:
            dfi_data = await dfi_service.get_movie_details(movie.dfi_id)
            if dfi_data:
                # Update cached data
                movie_data = dfi_service.parse_movie_data(dfi_data)
                for key, value in movie_data.model_dump().items():
                    if key != "id" and value is not None:
                        setattr(movie, key, value)
                movie.cached_at = datetime.now(timezone.utc)
                db.commit()
                db.refresh(movie)
        finally:
            await dfi_service.close()
    
    return movie
