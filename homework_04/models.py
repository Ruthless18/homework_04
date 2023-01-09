"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""
import os

from homework_04.mixins import CreatedAtMixin

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
    relationship,
)
from sqlalchemy import (
    Column,
    String,
    Integer,
)

PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://postgres:password@localhost/postgres"

async_engine: AsyncEngine = create_async_engine(
    url = PG_CONN_URI,
    echo = False,
)

Base = declarative_base()

Session = sessionmaker(
    async_engine,
    class_ = AsyncSession,
    expire_on_commit = False,
)


async def create_tables():
    async with async_engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)
        await connect.run_sync(Base.metadata.create_all)


async def create_users(user_data):
    async with Session() as session:
        async with session.begin():
            for user in user_data:
                username = user['username']
                email = user['email']
                user = User(username = username, email = email)
                session.add(user)


async def create_posts(post_data):
    async with Session() as session:
        async with session.begin():
            for post in post_data:
                id = post['id']
                title = post['title']
                description = post['body']
                post = Post(title = title, description = description, id = id)
                session.add(post)


class User(CreatedAtMixin, Base):
    __tablename__ = 'user'


    id = Column(
        Integer,
        primary_key = True
    )
    username = Column(
        String,
        nullable = False,
        default = '',
        server_default = '',
    )
    email = Column(
        String,
        nullable = False,
        default = '',
        server_default = '',
    )

    posts = relationship("Post", back_populates = "users", uselist = False)

    def __str__(self):
        return f"{self.__class__.__name__}(id = {self.id}, username = {self.username!r}," \
               f"email={self.email})"


    def __repr__(self):
        return str(self)


class Post(CreatedAtMixin, Base):
    __tablename__ = 'posts'


    id = Column(
        Integer,
        primary_key = True
    )
    title = Column(
        String,
        nullable = False,
        default = '',
        server_default = '',
    )
    description = Column(
        String,
        nullable = False,
        default = '',
        server_default = '',
    )

    users = relationship("User", back_populates = "posts", uselist = False)


    def __str__(self):
        return f"{self.__class__.__name__}(id= {self.id}, title = {self.title!r}," \
               f"description = {self.description!r})"


    def __repr__(self):
        return str(self)