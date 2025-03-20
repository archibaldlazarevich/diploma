from typing import Annotated, cast

from fastapi import Header
from sqlalchemy import Result, and_, delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import src.database.models as models


async def post_likes_module(
    id: int,
    session: AsyncSession,
    api_key: Annotated[str | None, Header()] = None,
) -> bool:
    """
    Модуль для обработки данных эндпоинта post /api/tweets/{id}/likes
    :param id: id твита, который получает лайк
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :param session: сессия для подключения к базе данных
    :return: bool
    """
    result: Result[tuple[models.Users]] = await session.execute(
        select(models.Users).where(models.Users.api_key == api_key)
    )

    user_id: models.Users = cast(models.Users, result.scalar())

    await session.execute(
        insert(models.Likes).values(
            user_id=cast(int, user_id.id), tweets_id=id
        )
    )
    await session.execute(
        update(models.Tweets)
        .where(models.Tweets.id == id)
        .values(tweets_likes=models.Tweets.tweets_likes + 1)
    )
    await session.commit()

    return True


async def delete_likes_module(
    id: int,
    session: AsyncSession,
    api_key: Annotated[str | None, Header()] = None,
) -> bool:
    """
    Модуль для обработки данных эндпоинта delete /api/tweets/{id}/likes
    :param id: id твита, который теряет лайк
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :param session: сессия для подключения к базе данных
    :return: bool
    """

    user_id: Result[tuple[models.Users]] = await session.execute(
        select(models.Users.id).where(models.Users.api_key == api_key)
    )

    await session.execute(
        delete(models.Likes).where(
            and_(
                models.Likes.tweets_id == id,
                models.Likes.user_id == user_id.scalar(),
            )
        )
    )

    await session.execute(
        update(models.Tweets)
        .where(models.Tweets.id == id)
        .values(tweets_likes=models.Tweets.tweets_likes - 1)
    )

    await session.commit()

    return True
