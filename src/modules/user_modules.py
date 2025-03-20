from typing import Annotated, cast

from fastapi import Header
from sqlalchemy import Result, and_, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import QueryableAttribute, joinedload

import src.database.models as models


async def post_users_follow_module(
    id: int,
    session: AsyncSession,
    api_key: Annotated[str | None, Header()] = None,
) -> bool:
    """
    Модуль по обработке данных для эндпоинта post /api/users/{id}/follow
    :param id: id пользователя, которого требуется добавить
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :param session: сессия для подключения к базе данных
    :return: bool
    """
    result: Result[tuple[models.Users]] = await session.execute(
        select(models.Users).where(models.Users.api_key == api_key)
    )

    follower: models.Users = cast(models.Users, result.scalar())

    await session.execute(
        insert(models.followers_tb).values(
            followed_id=id, follower_id=follower.id
        )
    )

    await session.commit()

    return True


async def delete_users_follow_module(
    id: int,
    session: AsyncSession,
    api_key: Annotated[str | None, Header()] = None,
) -> bool:
    """
    Модуль по обработке данных для эндпоинта delete /api/users/{id}/follow
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :param id: id пользователя, которого требуется добавить
    :param session: сессия для подключения к базе данных
    :return: bool
    """

    result: Result[tuple[models.Users]] = await session.execute(
        select(models.Users).where(models.Users.api_key == api_key)
    )

    follower: models.Users = cast(models.Users, result.scalar())

    await session.execute(
        delete(models.followers_tb).filter(
            and_(
                models.followers_tb.c.follower_id == follower.id,
                models.followers_tb.c.followed_id == id,
            )
        )
    )
    await session.commit()

    return True


async def get_user_module(
    session: AsyncSession,
    api_key: Annotated[str | None, Header()] = None,
    id: int | None = None,
) -> models.Users:
    """
    Модуль по обработке данных для эндпоинта
    get /api/users/me или /api/users/{id}
    :param id: id пользователя, по которому требуется получить данные
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :param session: сессия для подключения к базе данн
    :return:
    """
    if id is not None:
        user: Result[tuple[models.Users]] = await session.execute(
            select(models.Users)
            .where(models.Users.id == id)
            .options(
                joinedload(models.Users.followers).load_only(
                    cast(QueryableAttribute, models.Users.id),
                    cast(QueryableAttribute, models.Users.name),
                )
            )
            .options(
                joinedload(models.Users.followed).load_only(
                    cast(QueryableAttribute, models.Users.id),
                    cast(QueryableAttribute, models.Users.name),
                )
            )
        )

        return cast(models.Users, user.scalar())
    else:
        user_new: Result[tuple[models.Users]] = await session.execute(
            select(models.Users)
            .where(models.Users.api_key == api_key)
            .options(
                joinedload(models.Users.followers).load_only(
                    cast(QueryableAttribute, models.Users.id),
                    cast(QueryableAttribute, models.Users.name),
                )
            )
            .options(
                joinedload(models.Users.followed).load_only(
                    cast(QueryableAttribute, models.Users.id),
                    cast(QueryableAttribute, models.Users.name),
                )
            )
        )
        return cast(models.Users, user_new.scalar())
