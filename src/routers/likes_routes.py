from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

import src.modules.likes_modules as lik_mod
import src.schemas.schemas as sch
from src.database.create_db import get_db_session

router = APIRouter(prefix="/api", tags=["likes"])


@router.post("/tweets/{id}/likes", response_model=sch.Result)
async def post_tweet_like(
    id: int,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    api_key: Annotated[str | None, Header()] = None,
) -> dict:
    """
    Эндпоинт, описывающий процесс лайка твита
    :param session: сессия для подключения к базе данных
    :param id: id твита, который получает лайк
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :return: json-объект по типу:
        {“result”: true}, возвращающий статус операции
    """
    await lik_mod.post_likes_module(id=id, api_key=api_key, session=session)

    return {"result": True}


@router.delete("/tweets/{id}/likes", response_model=sch.Result)
async def delete_tweet_like(
    id: int,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    api_key: Annotated[str | None, Header()] = None,
) -> dict:
    """
    Эндпоинт, описывающий процесс удаления лайка твита
    :param session: сессия для подключения к базе данных
    :param id: id твита, который лишается лайка
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :return: json-объект по типу:
        {“result”: true}, возвращающий статус операции
    """
    await lik_mod.delete_likes_module(id=id, api_key=api_key, session=session)

    return {"result": True}
