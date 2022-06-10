from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, engine as engine_  # type: ignore
from sqlalchemy.orm import sessionmaker
from backend.config import get_settings
from typing import AsyncIterable, Callable


def gen_engine():
    engine = create_async_engine(
        get_settings().database_url,
        future=True,
        echo=True,
    )
    return engine


def gen_local_session(engine: engine_.AsyncEngine) -> Callable[..., AsyncSession]:
    session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore
    return session  # type: ignore


Engine = gen_engine()
SessionLocal = gen_local_session(Engine)  # type: ignore


async def get_db() -> AsyncIterable[AsyncSession]:
    db: AsyncSession = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
