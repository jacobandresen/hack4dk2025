from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.user import User
from app.models.collection import Collection, CollectionMovie
from app.models.movie import Movie
from app.services.auth_service import verify_token
from app.schemas.collection import (
    Collection as CollectionSchema,
    CollectionCreate,
    CollectionUpdate,
    CollectionDetail,
    CollectionMovie as CollectionMovieSchema,
    CollectionMovieAdd,
    CollectionMovieUpdate
)

router = APIRouter()

def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get current user from JWT token"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = authorization.split(" ")[1]
    payload = verify_token(token)
    
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    username = payload["sub"]
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user

@router.get("", response_model=List[CollectionSchema])
async def get_collections(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's collections"""
    collections = db.query(Collection).filter(Collection.user_id == current_user.id).all()
    return collections

@router.post("", response_model=CollectionSchema)
async def create_collection(
    collection_data: CollectionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new collection"""
    db_collection = Collection(
        user_id=current_user.id,
        name=collection_data.name,
        description=collection_data.description
    )
    
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    
    return db_collection

@router.get("/{collection_id}", response_model=CollectionDetail)
async def get_collection(
    collection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get collection details with movies"""
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Get movies in this collection
    collection_movies = db.query(CollectionMovie).filter(
        CollectionMovie.collection_id == collection_id
    ).all()
    
    return CollectionDetail(
        **collection.__dict__,
        movies=[CollectionMovieSchema.from_orm(cm) for cm in collection_movies]
    )

@router.put("/{collection_id}", response_model=CollectionSchema)
async def update_collection(
    collection_id: int,
    collection_data: CollectionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a collection"""
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    if collection_data.name is not None:
        collection.name = collection_data.name
    if collection_data.description is not None:
        collection.description = collection_data.description
    
    db.commit()
    db.refresh(collection)
    
    return collection

@router.delete("/{collection_id}")
async def delete_collection(
    collection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a collection"""
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    db.delete(collection)
    db.commit()
    
    return {"message": "Collection deleted"}

@router.post("/{collection_id}/movies", response_model=CollectionMovieSchema)
async def add_movie_to_collection(
    collection_id: int,
    movie_data: CollectionMovieAdd,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a movie to a collection"""
    # Check if collection exists and belongs to user
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Check if movie exists
    movie = db.query(Movie).filter(Movie.id == movie_data.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Check if movie is already in collection
    existing = db.query(CollectionMovie).filter(
        CollectionMovie.collection_id == collection_id,
        CollectionMovie.movie_id == movie_data.movie_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Movie already in collection")
    
    # Add movie to collection
    collection_movie = CollectionMovie(
        collection_id=collection_id,
        movie_id=movie_data.movie_id,
        note=movie_data.note
    )
    
    db.add(collection_movie)
    db.commit()
    db.refresh(collection_movie)
    
    return CollectionMovieSchema.from_orm(collection_movie)

@router.delete("/{collection_id}/movies/{movie_id}")
async def remove_movie_from_collection(
    collection_id: int,
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a movie from a collection"""
    # Check if collection exists and belongs to user
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Find and remove the movie from collection
    collection_movie = db.query(CollectionMovie).filter(
        CollectionMovie.collection_id == collection_id,
        CollectionMovie.movie_id == movie_id
    ).first()
    
    if not collection_movie:
        raise HTTPException(status_code=404, detail="Movie not found in collection")
    
    db.delete(collection_movie)
    db.commit()
    
    return {"message": "Movie removed from collection"}

@router.put("/{collection_id}/movies/{movie_id}", response_model=CollectionMovieSchema)
async def update_movie_note(
    collection_id: int,
    movie_id: int,
    movie_data: CollectionMovieUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update movie note in collection"""
    # Check if collection exists and belongs to user
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()
    
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Find the movie in collection
    collection_movie = db.query(CollectionMovie).filter(
        CollectionMovie.collection_id == collection_id,
        CollectionMovie.movie_id == movie_id
    ).first()
    
    if not collection_movie:
        raise HTTPException(status_code=404, detail="Movie not found in collection")
    
    # Update note
    collection_movie.note = movie_data.note
    db.commit()
    db.refresh(collection_movie)
    
    return CollectionMovieSchema.from_orm(collection_movie)
