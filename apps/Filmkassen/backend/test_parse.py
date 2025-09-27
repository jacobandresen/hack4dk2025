import asyncio
from app.services.dfi_service import DFIService

async def test_parse():
    service = DFIService()
    try:
        results = await service.search_movies("jagten")
        print(f"Found {len(results)} movies")
        if results:
            first_movie = results[0]
            print("Raw movie data:", first_movie)
            
            # Test parsing
            movie_data = service.parse_movie_data(first_movie)
            print("Parsed movie data:", movie_data.dict())
    except Exception as e:
        print("Parse error:", e)
    finally:
        await service.close()

asyncio.run(test_parse())
