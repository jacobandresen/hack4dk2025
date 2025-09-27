from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DirectorBase(BaseModel):
    name: str

class DirectorCreate(DirectorBase):
    dfi_id: Optional[str] = None
    bio: Optional[str] = None

class Director(DirectorBase):
    id: int
    dfi_id: Optional[str] = None
    bio: Optional[str] = None
    cached_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
