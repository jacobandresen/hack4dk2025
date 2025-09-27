from sqlalchemy import Column, String, DateTime, Boolean, Text, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from .database import Base

# Association table for many-to-many relationship between collections and artworks
collection_artworks = Table(
    'collection_artworks',
    Base.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('collection_id', UUID(as_uuid=True), ForeignKey('collections.id'), nullable=False),
    Column('artwork_id', UUID(as_uuid=True), ForeignKey('artworks.id'), nullable=False),
    Column('note', Text),
    Column('added_at', DateTime(timezone=True), server_default=func.now())
)

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    collections = relationship("Collection", back_populates="owner", cascade="all, delete-orphan")

class Artwork(Base):
    __tablename__ = "artworks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_number = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(500), nullable=True)
    year = Column(String(20), nullable=True)
    artist_name = Column(String(255), nullable=True)
    image_thumbnail = Column(String(1000), nullable=True)
    image_iiif_id = Column(String(1000), nullable=True)
    public_domain = Column(Boolean, default=False)
    object_names = Column(JSONB, nullable=True)
    has_image = Column(Boolean, default=False)
    cached_at = Column(DateTime(timezone=True), server_default=func.now())
    raw_data = Column(JSONB, nullable=True)

    # Relationships
    collections = relationship("Collection", secondary=collection_artworks, back_populates="artworks")

class Collection(Base):
    __tablename__ = "collections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="collections")
    artworks = relationship("Artwork", secondary=collection_artworks, back_populates="collections")
