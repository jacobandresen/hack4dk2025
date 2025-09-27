from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List
from uuid import UUID

from ..database import get_db
from ..models import User, Collection, Artwork, collection_artworks
from ..schemas import (
    Collection as CollectionSchema, 
    CollectionCreate, 
    CollectionUpdate,
    CollectionDetails,
    CollectionItem,
    CollectionItemCreate
)
from ..auth import get_current_user

router = APIRouter()

@router.get("", response_model=List[CollectionSchema])
async def get_user_collections(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all collections for the authenticated user"""
    collections = db.query(Collection).filter(Collection.user_id == current_user.id).all()
    return [CollectionSchema.from_orm(collection) for collection in collections]

@router.post("", response_model=CollectionSchema, status_code=201)
async def create_collection(
    collection_data: CollectionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new collection for the authenticated user"""
    # Check if collection name already exists for this user
    existing_collection = db.query(Collection).filter(
        and_(
            Collection.user_id == current_user.id,
            Collection.name == collection_data.name
        )
    ).first()
    
    if existing_collection:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Collection with this name already exists"
        )
    
    # Create new collection
    db_collection = Collection(
        name=collection_data.name,
        description=collection_data.description,
        user_id=current_user.id
    )
    
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    
    return CollectionSchema.from_orm(db_collection)

@router.get("/{collection_id}", response_model=CollectionDetails)
async def get_collection(
    collection_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of a specific collection including artworks"""
    collection = db.query(Collection).filter(
        and_(
            Collection.id == collection_id,
            Collection.user_id == current_user.id
        )
    ).first()
    
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )
    
    # Get collection items with artworks
    collection_items = db.query(collection_artworks).filter(
        collection_artworks.c.collection_id == collection_id
    ).all()
    
    items = []
    for item in collection_items:
        artwork = db.query(Artwork).filter(Artwork.id == item.artwork_id).first()
        if artwork:
            items.append(CollectionItem(
                id=item.id,
                artwork=artwork,
                note=item.note,
                added_at=item.added_at
            ))
    
    collection_details = CollectionDetails.from_orm(collection)
    collection_details.artworks = items
    
    return collection_details

@router.put("/{collection_id}", response_model=CollectionSchema)
async def update_collection(
    collection_id: UUID,
    collection_data: CollectionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update collection details"""
    collection = db.query(Collection).filter(
        and_(
            Collection.id == collection_id,
            Collection.user_id == current_user.id
        )
    ).first()
    
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )
    
    # Check if new name conflicts with existing collections
    if collection_data.name != collection.name:
        existing_collection = db.query(Collection).filter(
            and_(
                Collection.user_id == current_user.id,
                Collection.name == collection_data.name,
                Collection.id != collection_id
            )
        ).first()
        
        if existing_collection:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Collection with this name already exists"
            )
    
    # Update collection
    collection.name = collection_data.name
    collection.description = collection_data.description
    
    db.commit()
    db.refresh(collection)
    
    return CollectionSchema.from_orm(collection)

@router.delete("/{collection_id}", status_code=204)
async def delete_collection(
    collection_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a collection"""
    collection = db.query(Collection).filter(
        and_(
            Collection.id == collection_id,
            Collection.user_id == current_user.id
        )
    ).first()
    
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )
    
    db.delete(collection)
    db.commit()

@router.post("/{collection_id}/artworks", response_model=CollectionItem, status_code=201)
async def add_artwork_to_collection(
    collection_id: UUID,
    item_data: CollectionItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add an artwork to a collection with optional note"""
    # Check if collection exists and belongs to user
    collection = db.query(Collection).filter(
        and_(
            Collection.id == collection_id,
            Collection.user_id == current_user.id
        )
    ).first()
    
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )
    
    # Check if artwork exists
    artwork = db.query(Artwork).filter(Artwork.id == item_data.artwork_id).first()
    if not artwork:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artwork not found"
        )
    
    # Check if artwork is already in collection
    existing_item = db.query(collection_artworks).filter(
        and_(
            collection_artworks.c.collection_id == collection_id,
            collection_artworks.c.artwork_id == item_data.artwork_id
        )
    ).first()
    
    if existing_item:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Artwork already in collection"
        )
    
    # Add artwork to collection
    insert_stmt = collection_artworks.insert().values(
        collection_id=collection_id,
        artwork_id=item_data.artwork_id,
        note=item_data.note
    )
    result = db.execute(insert_stmt)
    db.commit()
    
    # Get the inserted item using the returned id
    inserted_id = result.inserted_primary_key[0]
    item = db.query(collection_artworks).filter(
        collection_artworks.c.id == inserted_id
    ).first()
    
    return CollectionItem(
        id=item.id,
        artwork=artwork,
        note=item.note,
        added_at=item.added_at
    )

@router.delete("/{collection_id}/artworks/{artwork_id}", status_code=204)
async def remove_artwork_from_collection(
    collection_id: UUID,
    artwork_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove an artwork from a collection"""
    # Check if collection exists and belongs to user
    collection = db.query(Collection).filter(
        and_(
            Collection.id == collection_id,
            Collection.user_id == current_user.id
        )
    ).first()
    
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found"
        )
    
    # Check if artwork is in collection
    item = db.query(collection_artworks).filter(
        and_(
            collection_artworks.c.collection_id == collection_id,
            collection_artworks.c.artwork_id == artwork_id
        )
    ).first()
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artwork not found in collection"
        )
    
    # Remove artwork from collection
    delete_stmt = collection_artworks.delete().where(
        and_(
            collection_artworks.c.collection_id == collection_id,
            collection_artworks.c.artwork_id == artwork_id
        )
    )
    db.execute(delete_stmt)
    db.commit()
