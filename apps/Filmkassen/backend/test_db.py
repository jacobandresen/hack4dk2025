from sqlalchemy import text
from app.core.database import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('Database connection test:', result.scalar())
except Exception as e:
    print('Database connection error:', e)
