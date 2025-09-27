# SMK MCP Server Implementation

This is a Python implementation of an MCP (Model Context Protocol) server that exposes resources from the SMK (Statens Museum for Kunst) API.

## Features

- **ArtSearch**: Search for artworks in the SMK collection
- **Detail**: Get detailed information about specific artworks

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python smk_mcp_server.py
```

## Usage

### ArtSearch Resource

Search for artworks using the `smk://artsearch` resource:

```
smk://artsearch?keys=amager&offset=0&rows=100
```

Parameters:
- `keys` (required): Search terms
- `offset` (optional): Starting position (default: 0)
- `rows` (optional): Number of results (default: 100, max: 100)

### Detail Resource

Get detailed information about a specific artwork using the `smk://detail` resource:

```
smk://detail?id=KMS1234
```

Parameters:
- `id` (required): Artwork ID

## API Mapping

The MCP server maps to the SMK API as follows:

- **Search**: `https://api.smk.dk/api/v1/art/search/`
- **Detail**: `https://api.smk.dk/api/v1/art/object/{id}`

## Testing

Run all tests:
```bash
python run_tests.py
```

Run specific test suites:
```bash
# Unit tests only
python -m pytest test_unit.py -v

# Integration tests only
python -m pytest test_integration.py -v

# Manual integration test
python test_integration.py
```

## Architecture

The implementation follows hexagonal architecture principles:

- **Domain Models**: `ArtworkSearchResult`, `ArtworkDetail`
- **API Client**: `SMKAPIClient` handles external API communication
- **MCP Server**: Exposes resources through the MCP protocol
- **Tests**: Comprehensive unit and integration tests

## Error Handling

- HTTP errors are caught and logged
- Invalid parameters return appropriate error messages
- Network timeouts are set to 30 seconds
- Graceful degradation when API is unavailable

## Data Model

### ArtworkSearchResult
- `id`: Artwork identifier
- `title`: Artwork title
- `year`: Production year (optional)
- `artist`: Artist name (optional)
- `image_url`: Thumbnail image URL (optional)

### ArtworkDetail
- All fields from ArtworkSearchResult
- `high_res_image_url`: High resolution image URL (optional)
- `description`: Artwork description (optional)

