from typing import Annotated, Sequence, Union, cast

from fastapi import Header
from sqlalchemy import Result, and_, delete, desc, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

import src.database.models as models


async def post_tweet_module(
    request: dict[str, Union[list[int], str]],
    session: AsyncSession,
    api_key: Annotated[str | None, Header()] = None,
) -> int:
    """
    Модуль по обработке данных для эндпоинта post /api/tweets
    :param request: запрос от сервера
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :param session: сессия для подключения к базе данных
    :return: id твита
    """

    tweet_data: str = cast(str, request.get("tweet_data"))
    tweet_media_ids: list[int] = cast(
        list[int], request.get("tweet_media_ids")
    )

    user_id: Result[tuple[models.Tweets]] = await session.execute(
        select(models.Users.id).where(models.Users.api_key == api_key)
    )

    if len(tweet_media_ids) != 0:
        tweets: Result[tuple[models.Tweets]] = await session.execute(
            insert(models.Tweets)
            .values(
                user_id=user_id.scalar(),
                tweets_data=tweet_data,
                tweet_media_ids=tweet_media_ids[0],
            )
            .returning(models.Tweets)
        )
        await session.commit()

        result: models.Tweets = cast(models.Tweets, tweets.scalar())
        return cast(int, result.id)

    tweets_without_media: Result[tuple[models.Tweets]] = await session.execute(
        insert(models.Tweets)
        .values(
            user_id=user_id.scalar(),
            tweets_data=tweet_data,
        )
        .returning(models.Tweets)
    )

    await session.commit()

    result_without_media: models.Tweets = cast(
        models.Tweets, tweets_without_media.scalar()
    )
    return cast(int, result_without_media.id)


async def delete_tweet_module(
    id: int,
    session: AsyncSession,
    api_key: Annotated[str | None, Header()] = None,
) -> models.Tweets | None:
    """
    Модуль по обработке данных для эндпоинта delete /api/tweets/{id}
    :param id: id твита, который требуется удалить
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :param session: сессия для подключения к базе данных
    :return: None или экземпляр класса models.Tweets
    """

    result: Result[tuple[models.Tweets]] = await session.execute(
        delete(models.Tweets)
        .filter(
            and_(
                models.Tweets.id == id,
                models.Tweets.user_id
                == select(models.Users.id)
                .where(models.Users.api_key == api_key)
                .scalar_subquery(),
            )
        )
        .returning(models.Tweets)
    )
    await session.commit()

    return result.scalar()


async def get_tweets_module(
    session: AsyncSession,
) -> list:
    """
    Модуль по обработке данных для эндпоинта get /api/tweets
    :param session: сессия для подключения к базе данных
    :return: list
    """

    tweets_data: Result[tuple[models.Tweets]] = await session.execute(
        select(models.Tweets)
        .options(
            joinedload(models.Tweets.user),
            joinedload(models.Tweets.like).subqueryload(models.Likes.user),
            joinedload(models.Tweets.media),
        )
        .group_by(models.Tweets.id)
        .order_by(desc(models.Tweets.tweets_likes))
    )

    tweets: Sequence[models.Tweets] = tweets_data.unique().scalars().all()

    return [
        {
            "id": tweet.id,
            "content": tweet.tweets_data,
            "attachments": (
                [f"/api/medias/{tweet.media.id}"]
                if tweet.media is not None
                else []
            ),
            "author": {"id": tweet.user.id, "name": tweet.user.name},
            "likes": [
                {"user_id": i.user_id, "name": i.user.name} for i in tweet.like
            ],
        }
        for tweet in tweets
    ]
