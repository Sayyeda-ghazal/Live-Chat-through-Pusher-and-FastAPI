from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.config import get_settings

from sqlalchemy.ext.declarative import declarative_base

settings = get_settings()
Base = declarative_base()

engine = create_engine(settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

with engine.connect() as connection:
    print("Database connection successful")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()