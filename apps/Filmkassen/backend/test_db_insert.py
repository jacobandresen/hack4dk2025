import asyncio
from app.services.dfi_service import DFIService
from app.core.database import SessionLocal
from app.models.movie import Movie

async def test_db_insert():
    service = DFIService()
    db = SessionLocal()
    try:
        results = await service.search_movies("jagten")
        if results:
            first_movie = results[0]
            movie_data = service.parse_movie_data(first_movie)
            
            # Check if movie already exists
            existing = db.query(Movie).filter(Movie.dfi_id == movie_data.dfi_id).first()
            if existing:
                print("Movie already exists:", existing.title)
            else:
                # Try to create new movie
                db_movie = Movie(**movie_data.dict())
                db.add(db_movie)
                db.commit()
                db.refresh(db_movie)
                print("Created movie:", db_movie.title)
    except Exception as e:
        print("Database error:", e)
        db.rollback()
    finally:
        await service.close()
        db.close()

asyncio.run(test_db_insert())
