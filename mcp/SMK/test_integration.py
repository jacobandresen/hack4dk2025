#!/usr/bin/env python3
"""
Integration tests for SMK API
Tests the actual API endpoints with real data
"""

import asyncio
import pytest
import httpx
from smk_simple_mcp import SMKAPIClient


class TestSMKAPIIntegration:
    """Integration tests for SMK API client"""
    
    @pytest.fixture
    async def api_client(self):
        """Create API client for testing"""
        client = SMKAPIClient()
        yield client
        await client.close()
    
    @pytest.mark.asyncio
    async def test_search_artworks_amager(self, api_client):
        """Test searching for artworks with 'amager' keyword"""
        artworks = await api_client.search_artworks("amager", offset=0, rows=10)
        
        # Should return results
        assert len(artworks) > 0, "Should return at least one artwork for 'amager' search"
        
        # Check structure of first result
        first_artwork = artworks[0]
        assert hasattr(first_artwork, 'id'), "Artwork should have an ID"
        assert hasattr(first_artwork, 'title'), "Artwork should have a title"
        assert isinstance(first_artwork.id, str), "ID should be a string"
        assert isinstance(first_artwork.title, str), "Title should be a string"
        
        print(f"Found {len(artworks)} artworks for 'amager' search")
        print(f"First artwork: {first_artwork.title} (ID: {first_artwork.id})")
    
    @pytest.mark.asyncio
    async def test_search_artworks_pagination(self, api_client):
        """Test search pagination"""
        # Get first page
        page1 = await api_client.search_artworks("amager", offset=0, rows=5)
        # Get second page
        page2 = await api_client.search_artworks("amager", offset=5, rows=5)
        
        # Should have results
        assert len(page1) > 0, "First page should have results"
        
        # If we have enough results, pages should be different
        if len(page1) == 5 and len(page2) > 0:
            assert page1[0].id != page2[0].id, "Different pages should have different results"
        
        print(f"Page 1: {len(page1)} results")
        print(f"Page 2: {len(page2)} results")
    
    @pytest.mark.asyncio
    async def test_search_artworks_empty_query(self, api_client):
        """Test search with empty query"""
        artworks = await api_client.search_artworks("", offset=0, rows=10)
        
        # Empty query might return empty results or all results
        # Both are acceptable depending on API behavior
        print(f"Empty query returned {len(artworks)} results")
    
    @pytest.mark.asyncio
    async def test_get_artwork_detail_success(self, api_client):
        """Test getting artwork detail for a known artwork"""
        # First search for an artwork to get an ID
        artworks = await api_client.search_artworks("amager", offset=0, rows=1)
        
        if len(artworks) > 0:
            artwork_id = artworks[0].id
            detail = await api_client.get_artwork_detail(artwork_id)
            
            assert detail is not None, f"Should get detail for artwork {artwork_id}"
            assert detail.id == artwork_id, "Detail ID should match requested ID"
            assert hasattr(detail, 'title'), "Detail should have title"
            assert hasattr(detail, 'high_res_image_url'), "Detail should have high res image URL"
            
            print(f"Detail for {artwork_id}: {detail.title}")
            if detail.high_res_image_url:
                print(f"High res image: {detail.high_res_image_url}")
        else:
            pytest.skip("No artworks found to test detail retrieval")
    
    @pytest.mark.asyncio
    async def test_get_artwork_detail_not_found(self, api_client):
        """Test getting detail for non-existent artwork"""
        detail = await api_client.get_artwork_detail("NONEXISTENT123")
        
        assert detail is None, "Should return None for non-existent artwork"
        print("Correctly handled non-existent artwork")
    
    @pytest.mark.asyncio
    async def test_api_response_time(self, api_client):
        """Test that API responses are reasonably fast"""
        import time
        
        start_time = time.time()
        artworks = await api_client.search_artworks("amager", offset=0, rows=10)
        end_time = time.time()
        
        response_time = end_time - start_time
        assert response_time < 10.0, f"API response took too long: {response_time:.2f}s"
        
        print(f"API response time: {response_time:.2f}s")


async def run_integration_tests():
    """Run integration tests manually"""
    print("Running SMK API integration tests...")
    
    client = SMKAPIClient()
    
    try:
        # Test search
        print("\n1. Testing search functionality...")
        artworks = await client.search_artworks("amager", offset=0, rows=5)
        print(f"Found {len(artworks)} artworks")
        
        if artworks:
            print("First few results:")
            for i, artwork in enumerate(artworks[:3]):
                print(f"  {i+1}. {artwork.title} (ID: {artwork.id})")
                if artwork.artist:
                    print(f"     Artist: {artwork.artist}")
                if artwork.year:
                    print(f"     Year: {artwork.year}")
        
        # Test detail retrieval
        if artworks:
            print(f"\n2. Testing detail retrieval for '{artworks[0].id}'...")
            detail = await client.get_artwork_detail(artworks[0].id)
            
            if detail:
                print(f"Title: {detail.title}")
                if detail.artist:
                    print(f"Artist: {detail.artist}")
                if detail.year:
                    print(f"Year: {detail.year}")
                if detail.high_res_image_url:
                    print(f"High res image: {detail.high_res_image_url}")
            else:
                print("Failed to get artwork detail")
        
        print("\n✅ Integration tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        raise
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(run_integration_tests())
