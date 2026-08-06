from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import DATABASE_URL

# SQLite needs this option because request handlers may use separate threads.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """Provide a transaction-scoped database session for future routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
