import os
from typing import cast

from fastapi import UploadFile
from sqlalchemy import Result, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import src.database.models as models


async def post_media_modules(
    session: AsyncSession,
    file: UploadFile,
) -> int:
    """
    Модуль по обработке данных для эндпоинта post /api/medias
    :param file: файл, прикрепленный пользователем для отправки в твите
    :param session: сессия для подключения к базе данных
    :return: id файла
    """

    file_dir: str = f"{os.getcwd()}/src/images/{file.filename}"

    with open(file_dir, "wb") as f:
        f.write(await file.read())

    media_id: Result[tuple[models.Medias]] = await session.execute(
        insert(models.Medias).values(path=file_dir).returning(models.Medias)
    )
    await session.commit()
    result: models.Medias = cast(models.Medias, media_id.scalar())

    return cast(int, result.id)


async def get_media_modules(
    id: int,
    session: AsyncSession,
) -> str:
    """
    Модуль по обработке данных для эндпоинта get /api/medias
    :param id: id
    :param session:
    :return: str -путь к файлу
    """

    result: Result[tuple[models.Medias]] = await session.execute(
        select(models.Medias).where(models.Medias.id == id)
    )

    path: models.Medias = cast(models.Medias, result.scalar())

    return cast(str, path.path)
