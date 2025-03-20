from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import src.modules.user_modules as user_mod
import src.schemas.schemas as sch
from src.database.create_db import get_db_session
from src.database.models import Users

router = APIRouter(prefix="/api", tags=["user"])


@router.post("/users/{id}/follow", response_model=sch.Result)
async def post_follow_user(
    id: int,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    api_key: Annotated[str | None, Header()] = None,
):
    """
    Эндпоинт, описывающий процесс подписки на пользователя
    :param session: сессия для подключения к базе данных
    :param id: id пользователя, на которого подписываются
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :return: json-объект по типу:
        {“result”: true}, возвращающий статус операции
    """

    await user_mod.post_users_follow_module(
        id=id, api_key=api_key, session=session
    )

    return {"result": True}


@router.delete("/users/{id}/follow", response_model=sch.Result)
async def delete_follow_user(
    id: int,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    api_key: Annotated[str | None, Header()] = None,
):
    """
    Эндпоинт, описывающий процесс отписки от пользователя
    :param session: сессия для подключения к базе данных
    :param api_key: ключ, передаваемы в headers запроса (опционально - test)
    :param id: id пользователя, орт которого требуется отписаться
    :return: json-объект по типу:
        {“result”: true}, возвращающий статус операции
    """

    await user_mod.delete_users_follow_module(
        id=id, api_key=api_key, session=session
    )

    return {"result": True}


@router.get("/users/me", response_model=sch.GetUser)
async def get_user_yourself_data(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    api_key: Annotated[str | None, Header()] = None,
):
    """
    Эндпоинт, описывающий процесс получения информации
    пользователем о самом себе
    :param session: сессия для подключения к базе данных
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :return: json-объект со списком данных о самом себе
    """

    user = await user_mod.get_user_module(api_key=api_key, session=session)

    if user is None:
        raise HTTPException(status_code=403)
    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [
                {"id": i.id, "name": i.name} for i in user.followers
            ],
            "following": [{"id": i.id, "name": i.name} for i in user.followed],
        },
    }


@router.get("/users/{id}", response_model=sch.GetUser)
async def get_user_data_by_id(
    id: int,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    api_key: Annotated[str | None, Header()] = None,
):
    """
    Эндпоинт, описывающий процесс получения
    информации пользователем о другом пользователе
    :param session: сессия для подключения к базе данных
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :param id: id пользователя, по которому требуется получить данные
    :return: json-объект со списком данных о запрашиваемом пользователе
    """
    user: Users | None = await user_mod.get_user_module(id=id, session=session)

    if user is None:
        raise HTTPException(status_code=403)
    return {
        "result": True,
        "user": {
            "id": user.id,
            "name": user.name,
            "followers": [
                {"id": i.id, "name": i.name} for i in user.followers
            ],
            "following": [{"id": i.id, "name": i.name} for i in user.followed],
        },
    }
