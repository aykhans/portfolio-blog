from sqlalchemy import (
    create_engine,
    Engine
)
from sqlalchemy.orm import (
    sessionmaker,
    Session
)
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession
)

from app.core.config import settings


engine: Engine = create_engine(
    str(settings.get_postgres_dsn()),
    pool_pre_ping=True
)
SessionLocal: Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

async_engine: AsyncEngine = create_async_engine(
    str(settings.get_postgres_dsn(_async=True)),
    future=True
)
AsyncSessionLocal: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)