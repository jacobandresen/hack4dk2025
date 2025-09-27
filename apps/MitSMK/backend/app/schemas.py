from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

# User schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

# Artwork schemas
class ArtworkBase(BaseModel):
    object_number: str
    title: Optional[str] = None
    year: Optional[str] = None
    artist_name: Optional[str] = None
    image_thumbnail: Optional[str] = None
    image_iiif_id: Optional[str] = None
    public_domain: bool = False
    object_names: Optional[List[str]] = None
    has_image: bool = False

class Artwork(ArtworkBase):
    id: UUID
    cached_at: datetime

    class Config:
        from_attributes = True

class ArtworkSearchResponse(BaseModel):
    artworks: List[Artwork]
    total: int
    offset: int
    limit: int

# Collection schemas
class CollectionBase(BaseModel):
    name: str
    description: Optional[str] = None

class CollectionCreate(CollectionBase):
    pass

class CollectionUpdate(CollectionBase):
    pass

class Collection(CollectionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CollectionItem(BaseModel):
    id: UUID
    artwork: Artwork
    note: Optional[str] = None
    added_at: datetime

    class Config:
        from_attributes = True

class CollectionDetails(Collection):
    artworks: List[CollectionItem]

class CollectionItemCreate(BaseModel):
    artwork_id: UUID
    note: Optional[str] = None
