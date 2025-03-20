from typing import Annotated, Union

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

import src.database.models as models
import src.modules.tweets_modules as tw_mod
import src.schemas.schemas as sch
from src.database.create_db import get_db_session

router = APIRouter(prefix="/api", tags=["tweets"])


@router.post("/tweets", response_model=sch.Tweets)
async def post_tweet(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    api_key: Annotated[str | None, Header()] = None,
) -> dict:
    """
    Эндпоинт, описывающий процесс создания пользователем нового твита,
    а так же сохранения этого твита
    :param session: сессия для подключения к базе данных
    :param request: запрос от сервера
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :return: json-объект по типу:
        {“result”: true,
        “tweet_id”: int}, возвращающий id твита
    """
    request_result: dict[str, Union[list[int], str]] = await request.json()

    result: int = await tw_mod.post_tweet_module(
        request=request_result, api_key=api_key, session=session
    )

    return {"result": True, "tweets_id": result}


@router.delete("/tweets/{id}", response_model=sch.Result)
async def delete_tweet(
    id: int,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    api_key: Annotated[str | None, Header()] = None,
) -> dict:
    """
    Эндпоинт, описывающий процесс удаления твита
    :param session: сессия для подключения к базе данных
    :param api_key: ключ, передаваемый в headers запроса (опционально - test)
    :param id: id твита, который требуется удалить
    :return: json-объект по типу:
        {“result”: true}, возвращающий статус операции
    """

    result: models.Tweets | None = await tw_mod.delete_tweet_module(
        id=id, api_key=api_key, session=session
    )

    if result is None:
        raise HTTPException(status_code=403)
    return {"result": True}


@router.get("/tweets", response_model=sch.TweetsSchema)
async def get_tweets(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    api_key: Annotated[str | None, Header()] = None,
) -> dict:
    """
    Эндпоинт, описывающий процесс получения пользователем ленты с твитами
    :param session: сессия для подключения к базе данных
    :param api_key: ключ, передаваемы в headers запроса (опционально - test)
    :return: json-объект со списком твитов для ленты этого пользователя
    """

    answer: list = await tw_mod.get_tweets_module(session=session)

    return {"result": True, "tweets": answer}
