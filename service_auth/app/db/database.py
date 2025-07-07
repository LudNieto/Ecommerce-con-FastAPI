from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings
from typing import Generator

DATABASE_URL = (f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
                f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")

engine = create_engine(DATABASE_URL, echo=True)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()