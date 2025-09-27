from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    dfi_id = Column(Integer, unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    year = Column(Integer)
    poster_url = Column(String(500))
    director = Column(String(255))
    cast = Column(JSON)
    clips = Column(JSON)
    videotek_url = Column(String(500))
    description = Column(Text)
    cached_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
