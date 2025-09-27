from app.core.database import engine
from app.models import Base

# Drop all tables first
Base.metadata.drop_all(bind=engine)
print("Dropped all tables")

# Create all tables
Base.metadata.create_all(bind=engine)
print("Created all tables successfully!")
