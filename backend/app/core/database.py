from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from redis import Redis
import asyncio
from typing import AsyncGenerator
from app.core.config import settings

# Database URL for async operations
ASYNC_DATABASE_URL = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create sync engine for migrations
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.ENVIRONMENT == "development",
    pool_pre_ping=True,
    pool_recycle=300,
)

# Session factories
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Redis client
redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)

async def init_db():
    """Initialize database tables"""
    async with async_engine.begin() as conn:
        # Import all models to ensure they're registered
        from app.models import user, entry, bookmark
        
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_db() -> Session:
    """Dependency to get sync database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def close_db():
    """Close database connections"""
    await async_engine.dispose()
    engine.dispose()
    redis_client.close()
