#!/usr/bin/env python3
"""
Unit tests for SMK MCP Server core functionality
"""

import pytest
import json
import httpx
from unittest.mock import AsyncMock, patch
from smk_simple_mcp import SMKAPIClient, ArtworkSearchResult, ArtworkDetail


class TestArtworkModels:
    """Test Pydantic models"""
    
    def test_artwork_search_result_creation(self):
        """Test ArtworkSearchResult model creation"""
        artwork = ArtworkSearchResult(
            id="KMS1234",
            title="Test Artwork",
            year="2020",
            artist="Test Artist",
            image_url="http://example.com/image.jpg"
        )
        
        assert artwork.id == "KMS1234"
        assert artwork.title == "Test Artwork"
        assert artwork.year == "2020"
        assert artwork.artist == "Test Artist"
        assert artwork.image_url == "http://example.com/image.jpg"
    
    def test_artwork_search_result_optional_fields(self):
        """Test ArtworkSearchResult with optional fields"""
        artwork = ArtworkSearchResult(
            id="KMS1234",
            title="Test Artwork"
        )
        
        assert artwork.id == "KMS1234"
        assert artwork.title == "Test Artwork"
        assert artwork.year is None
        assert artwork.artist is None
        assert artwork.image_url is None
    
    def test_artwork_detail_creation(self):
        """Test ArtworkDetail model creation"""
        artwork = ArtworkDetail(
            id="KMS1234",
            title="Test Artwork",
            year="2020",
            artist="Test Artist",
            image_url="http://example.com/thumb.jpg",
            high_res_image_url="http://example.com/full.jpg",
            description="A test artwork"
        )
        
        assert artwork.id == "KMS1234"
        assert artwork.title == "Test Artwork"
        assert artwork.year == "2020"
        assert artwork.artist == "Test Artist"
        assert artwork.image_url == "http://example.com/thumb.jpg"
        assert artwork.high_res_image_url == "http://example.com/full.jpg"
        assert artwork.description == "A test artwork"


class TestSMKAPIClient:
    """Test SMK API client with mocked responses"""
    
    @pytest.fixture
    def mock_response_data(self):
        """Mock API response data"""
        return {
            "items": [
                {
                    "object_number": "KMS1234",
                    "title": "Test Artwork 1",
                    "production_date": {"year": "2020"},
                    "creator": [{"name": "Test Artist 1"}],
                    "image_url": {"thumbnail": "http://example.com/thumb1.jpg"}
                },
                {
                    "object_number": "KMS5678",
                    "title": "Test Artwork 2",
                    "production_date": {"year": "2021"},
                    "creator": [{"name": "Test Artist 2"}],
                    "image_url": {"thumbnail": "http://example.com/thumb2.jpg"}
                }
            ]
        }
    
    @pytest.fixture
    def mock_detail_data(self):
        """Mock detail API response data"""
        return {
            "object_number": "KMS1234",
            "title": "Test Artwork Detail",
            "production_date": {"year": "2020"},
            "creator": [{"name": "Test Artist"}],
            "image_url": {
                "thumbnail": "http://example.com/thumb.jpg",
                "full": "http://example.com/full.jpg"
            },
            "description": "A detailed test artwork"
        }
    
    @pytest.mark.asyncio
    async def test_search_artworks_success(self, mock_response_data):
        """Test successful artwork search"""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status = AsyncMock(return_value=None)
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client
            
            client = SMKAPIClient()
            artworks = await client.search_artworks("test", offset=0, rows=10)
            
            assert len(artworks) == 2
            assert artworks[0].id == "KMS1234"
            assert artworks[0].title == "Test Artwork 1"
            assert artworks[0].year == "2020"
            assert artworks[0].artist == "Test Artist 1"
            assert artworks[0].image_url == "http://example.com/thumb1.jpg"
            
            await client.close()
    
    @pytest.mark.asyncio
    async def test_search_artworks_http_error(self):
        """Test search with HTTP error"""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.side_effect = httpx.HTTPError("Connection error")
            mock_client_class.return_value = mock_client
            
            client = SMKAPIClient()
            artworks = await client.search_artworks("test")
            
            assert len(artworks) == 0
            
            await client.close()
    
    @pytest.mark.asyncio
    async def test_search_artworks_empty_response(self):
        """Test search with empty response"""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_response = AsyncMock()
            mock_response.json.return_value = {"items": []}
            mock_response.raise_for_status = AsyncMock(return_value=None)
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client
            
            client = SMKAPIClient()
            artworks = await client.search_artworks("test")
            
            assert len(artworks) == 0
            
            await client.close()
    
    @pytest.mark.asyncio
    async def test_get_artwork_detail_success(self, mock_detail_data):
        """Test successful artwork detail retrieval"""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_response = AsyncMock()
            mock_response.json.return_value = mock_detail_data
            mock_response.raise_for_status = AsyncMock(return_value=None)
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client
            
            client = SMKAPIClient()
            artwork = await client.get_artwork_detail("KMS1234")
            
            assert artwork is not None
            assert artwork.id == "KMS1234"
            assert artwork.title == "Test Artwork Detail"
            assert artwork.year == "2020"
            assert artwork.artist == "Test Artist"
            assert artwork.image_url == "http://example.com/thumb.jpg"
            assert artwork.high_res_image_url == "http://example.com/full.jpg"
            assert artwork.description == "A detailed test artwork"
            
            await client.close()
    
    @pytest.mark.asyncio
    async def test_get_artwork_detail_http_error(self):
        """Test detail retrieval with HTTP error"""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.side_effect = httpx.HTTPError("Connection error")
            mock_client_class.return_value = mock_client
            
            client = SMKAPIClient()
            artwork = await client.get_artwork_detail("KMS1234")
            
            assert artwork is None
            
            await client.close()
    
    @pytest.mark.asyncio
    async def test_get_artwork_detail_not_found(self):
        """Test detail retrieval for non-existent artwork"""
        with patch('httpx.AsyncClient') as mock_client_class:
            mock_client = AsyncMock()
            mock_response = AsyncMock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Not Found", request=AsyncMock(), response=AsyncMock()
            )
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client
            
            client = SMKAPIClient()
            artwork = await client.get_artwork_detail("NONEXISTENT")
            
            assert artwork is None
            
            await client.close()


class TestMCPResourceHandling:
    """Test MCP resource handling logic"""
    
    def test_parse_search_uri(self):
        """Test parsing search URI with parameters"""
        from urllib.parse import parse_qs, urlparse
        
        uri = "smk://artsearch?keys=amager&offset=10&rows=50"
        parsed = urlparse(uri)
        params = parse_qs(parsed.query)
        
        assert params["keys"][0] == "amager"
        assert params["offset"][0] == "10"
        assert params["rows"][0] == "50"
    
    def test_parse_detail_uri(self):
        """Test parsing detail URI with parameters"""
        from urllib.parse import parse_qs, urlparse
        
        uri = "smk://detail?id=KMS1234"
        parsed = urlparse(uri)
        params = parse_qs(parsed.query)
        
        assert params["id"][0] == "KMS1234"
    
    def test_parse_uri_missing_params(self):
        """Test parsing URI with missing parameters"""
        from urllib.parse import parse_qs, urlparse
        
        uri = "smk://artsearch"
        parsed = urlparse(uri)
        params = parse_qs(parsed.query)
        
        assert params.get("keys", [""])[0] == ""
        assert params.get("offset", ["0"])[0] == "0"
        assert params.get("rows", ["100"])[0] == "100"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
