from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..core.config import settings

# Create engine for SQLite
engine = create_engine(
    settings.DATABASE_URI,
    connect_args={"check_same_thread": False},
    echo=True,
    future=True
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
