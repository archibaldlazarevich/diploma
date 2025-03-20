from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from config.config import DATABASE_URL, TEST_URL
from src.app import app
from src.database.create_db import Base, get_db_session
from src.database.models import Likes, Medias, Tweets, Users, followers_tb

from .answer_for_test import followed_data, likes, media, tweets, users

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
)

TestingSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def override_get_db_session():
    """Фикстура, которая возвращает сессию"""
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db_session] = override_get_db_session


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура для работы эндпоинтов на тестовом адресе"""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url=TEST_URL,
        trust_env=False,
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db():
    """Фикстура для создания базы данных при работе каждого теста"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(insert(Users), users)
        await conn.execute(insert(Medias), media)
        await conn.execute(insert(Tweets), tweets)
        await conn.execute(insert(Likes), likes)
        await conn.execute(insert(followers_tb), followed_data)
        await conn.commit()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
