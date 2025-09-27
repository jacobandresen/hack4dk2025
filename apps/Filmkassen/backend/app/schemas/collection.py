from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .movie import MovieSummary

class CollectionBase(BaseModel):
    name: str
    description: Optional[str] = None

class CollectionCreate(CollectionBase):
    pass

class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Collection(CollectionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CollectionMovieAdd(BaseModel):
    movie_id: int
    note: Optional[str] = None

class CollectionMovieUpdate(BaseModel):
    note: Optional[str] = None

class CollectionMovie(BaseModel):
    id: int
    movie: MovieSummary
    note: Optional[str] = None
    added_at: datetime
    
    class Config:
        from_attributes = True

class CollectionDetail(Collection):
    movies: List[CollectionMovie] = []
