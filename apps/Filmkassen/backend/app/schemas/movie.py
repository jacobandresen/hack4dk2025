from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MovieBase(BaseModel):
    title: str
    year: Optional[int] = None
    poster_url: Optional[str] = None
    director: Optional[str] = None

class MovieCreate(MovieBase):
    dfi_id: int
    cast: Optional[List[str]] = None
    clips: Optional[List[str]] = None
    videotek_url: Optional[str] = None
    description: Optional[str] = None

class MovieSummary(MovieBase):
    id: int
    dfi_id: int
    
    class Config:
        from_attributes = True

class Movie(MovieBase):
    id: int
    dfi_id: int
    cast: Optional[List[str]] = None
    clips: Optional[List[str]] = None
    videotek_url: Optional[str] = None
    description: Optional[str] = None
    cached_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
