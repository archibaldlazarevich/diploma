import asyncio
from typing import AsyncGenerator

import factory
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from config.config import DATABASE_URL

from .models import Base, Likes, Medias, Tweets, Users

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    # echo=True,
    poolclass=NullPool,
)

async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

faker = factory.Faker


async def get_db_session() -> AsyncGenerator:
    """
    Функция для работы с базой данный в эндпоинте
    :return: None
    """
    async with async_session_maker() as session:
        yield session


async def create_db() -> None:
    """
    Метод для создания базы данных
    :return: None
    """
    users_list: list[Users] = [
        Users(
            name=faker("first_name").evaluate(None, None, {"locale": "ru"}),
            api_key=f"{i}",
        )
        for i in range(3)
    ]
    users_list.append(Users(name="Test", api_key="test"))

    media_list: list[Medias] = [
        Medias(path="/app/src/images/photo.jpg") for i in range(3)
    ]

    tweets_list: list[Tweets] = [
        Tweets(
            user_id=i, tweets_likes=1, tweets_data="data", tweet_media_ids=i
        )
        for i in range(1, 4)
    ]

    likes_list: list[Likes] = [
        Likes(user_id=i, tweets_id=i) for i in range(1, 4)
    ]

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker.begin() as session:
        session.add_all(users_list)
        session.add_all(media_list)
        session.add_all(tweets_list)
        session.add_all(likes_list)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(create_db())
