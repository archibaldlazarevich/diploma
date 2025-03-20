from typing import Annotated

from fastapi import APIRouter, Depends, Header, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

import src.modules.medias_modules as med_mod
import src.schemas.schemas as sch
from src.database.create_db import get_db_session

router = APIRouter(prefix="/api", tags=["medias"])


@router.post("/medias", response_model=sch.Medias)
async def post_media(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    file: UploadFile,
    api_key: Annotated[str | None, Header()] = None,
) -> dict:
    """
    Эндпоинт, описывающий процесс загрузки файлов из твита,
    загрузка происходит через отправку формы.
    :param session: сессия для подключения к базе данных
    :param file: файл для загрузки
    :param api_key api_key: ключ, передаваемый
    в headers запроса (опционально - test)
    :return: json-объект по типу:
        {“result”: true,
        “media_id”: int}, возвращающий id загруженного файла
    """

    media_id: int = await med_mod.post_media_modules(
        file=file, session=session
    )

    return {"result": True, "media_id": media_id}


@router.get("/medias/{id}")
async def get_image_by_id(
    id: int,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    api_key: Annotated[str | None, Header()] = None,
) -> FileResponse:
    """
    Эндпоинт, описывающий процесс получения картинки по её id
    :param id: id файла, который требуется получить
    :param session: сессия для подключения к базе данных
    :param api_key: api_key пользователя
    :return: файл
    """
    path: str = await med_mod.get_media_modules(id=id, session=session)

    return FileResponse(path)
