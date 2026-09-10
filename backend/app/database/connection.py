from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db() -> Generator[Session, None, None]:
    """Provide a database session for a request and close it afterward."""
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
