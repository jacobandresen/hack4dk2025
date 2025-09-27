from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas import Artwork, ArtworkSearchResponse
from ..smk_service import SMKService

router = APIRouter()
smk_service = SMKService()

@router.get("/search", response_model=ArtworkSearchResponse)
async def search_artworks(
    q: str = Query(..., description="Search query"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(20, ge=1, le=100, description="Number of results to return"),
    db: Session = Depends(get_db)
):
    """Search for artworks using SMK API"""
    if not q.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query cannot be empty"
        )
    
    try:
        # Search and cache artworks
        artworks = await smk_service.search_and_cache_artworks(q, offset, limit, db)
        
        # Get total count from SMK API for pagination
        search_result = await smk_service.search_artworks(q, 0, 1)
        total = search_result.get("found", len(artworks))
        
        return ArtworkSearchResponse(
            artworks=artworks,
            total=total,
            offset=offset,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching artworks: {str(e)}"
        )

@router.get("/{object_number}", response_model=Artwork)
async def get_artwork(
    object_number: str,
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific artwork"""
    try:
        artwork = await smk_service.get_artwork_by_object_number(object_number, db)
        
        if not artwork:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Artwork not found"
            )
        
        return artwork
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching artwork: {str(e)}"
        )

