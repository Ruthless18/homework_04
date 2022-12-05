"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""
#import os
import config


from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,

)
from user import User
from post import Post


#PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") or "postgresql+asyncpg://postgres:password@localhost/postgres"

async_engine: AsyncEngine = create_async_engine(
    url = config.DB_ASYNC_URL,
    echo = config.DB_ECHO,
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
