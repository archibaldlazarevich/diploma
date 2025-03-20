from typing import List

from pydantic import BaseModel, ConfigDict


class Result(BaseModel):
    """
    Класс, описывающий общие данные для всех эндпоинтов
    """

    result: bool


class Tweets(Result):
    """
    Класс, описывающий данные для эндпоинта tweets
    """

    tweets_id: int

    class MyModel(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)


class Medias(Result):
    """
    Класс, описывающий данные для эндпоинта medias
    """

    media_id: int

    class MyModel(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)


class Author(BaseModel):
    """
    Класс, описывающий автора твита
    """

    id: int
    name: str


class Likes(BaseModel):
    """
    Класс, описывающий информацию о лайках на твитах
    """

    user_id: int
    name: str


class TweetsForGet(BaseModel):
    """
    Класс, описывающий твит для класса с лентой твитов
    """

    id: int
    content: str
    attachments: List[str]
    author: Author
    likes: List[Likes]


class TweetsSchema(Result):
    """
    Класс, описывающий общую схему ответа ленты с твитами
    """

    tweets: List[TweetsForGet]

    class MyModel(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)


class Follower(BaseModel):
    """
    Класс, описывающий информацию о подписчике/подписках
    """

    id: int
    name: str


class User(BaseModel):
    """
    Класс, описывающий информацию о пользователе
    """

    id: int
    name: str
    followers: List[Follower]
    following: List[Follower]


class GetUser(Result):
    """
    Класс, описывающий схему ответа при запросе о своей или чужом профиле
    """

    user: User

    class MyModel(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)
