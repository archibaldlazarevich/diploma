from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """
    Базовый класс для создания таблицы
    """


followers_tb = Table(
    "follower_tb",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("followed_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class Users(Base):
    """
    Класс, описывающий таблицу пользователей `users`
    с колонкой user_name - имя пользователя,
    user_key - ключ пользоваетеля для входа на сайт
    """

    __tablename__ = "users"

    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String, nullable=False)
    api_key: Column = Column(String, nullable=False, unique=True)
    tweet = relationship(argument="Tweets", back_populates="user")
    like = relationship(argument="Likes", back_populates="user")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    followers = relationship(
        "Users",
        secondary=followers_tb,
        primaryjoin=followers_tb.c.followed_id == id,
        secondaryjoin=followers_tb.c.follower_id == id,
        back_populates="followed",
    )
    followed = relationship(
        "Users",
        secondary=followers_tb,
        primaryjoin=followers_tb.c.follower_id == id,
        secondaryjoin=followers_tb.c.followed_id == id,
        back_populates="followers",
    )


class Tweets(Base):
    """
    Класс, описывающий таблицу твитов `tweets`
    с колонками user_id - id пользователя, добавившего твит
    tweets_likes - количество лайков у твита
    tweets_data - текстовое сообщение твита
    tweets_media_ids - id картинки, публикуемой в твите
    """

    __tablename__ = "tweets"

    id: Column = Column(Integer, primary_key=True)
    user_id: Column = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    tweets_likes: Column = Column(Integer, default=0)
    tweets_data: Column = Column(String, nullable=False)
    tweet_media_ids: Column = Column(
        Integer, ForeignKey("media.id", ondelete="CASCADE")
    )
    user = relationship(
        argument="Users",
        back_populates="tweet",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    media = relationship(argument="Medias", back_populates="tweet")
    like = relationship(argument="Likes", back_populates="tweet")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Likes(Base):
    """
    Класс, описывающий таблицу `likes`
    с колонками user_id - id пользователя, поставившего лайк
    tweets_id - id твита, который лайкнули
    """

    __tablename__ = "likes"

    id: Column = Column(Integer, primary_key=True)
    user_id: Column = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    tweets_id: Column = Column(
        Integer, ForeignKey("tweets.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship(
        argument="Users",
        back_populates="like",
        single_parent=True,
        foreign_keys=[user_id],
    )
    tweet = relationship(
        argument="Tweets", back_populates="like", single_parent=True
    )

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Medias(Base):
    """
    Класс, описывающий таблицу `media`
    с колонками - tweets_id - id твита, в котором опубликована картинка
    users_id - id пользователя, который опубликовал картинку
    """

    __tablename__ = "media"

    id: Column = Column(Integer, primary_key=True)
    path: Column = Column(String, nullable=False)
    tweet = relationship(argument="Tweets", back_populates="media")

    def to_json(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
