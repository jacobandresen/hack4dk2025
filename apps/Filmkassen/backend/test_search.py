import asyncio
from app.services.dfi_service import DFIService

async def test_search():
    service = DFIService()
    try:
        results = await service.search_movies("jagten")
        print(f"Found {len(results)} movies")
        if results:
            print("First movie:", results[0])
    except Exception as e:
        print("Search error:", e)
    finally:
        await service.close()

asyncio.run(test_search())
