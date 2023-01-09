"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""
from datetime import datetime



from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
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
    DateTime,
    ForeignKey,
    func
)

PG_ASYNC_CONN_URI = "postgresql+asyncpg://username:passwd!@localhost:5432/blog"

engine = create_async_engine(
    url = PG_ASYNC_CONN_URI,
    echo = False,
)

Base = declarative_base()

Session = sessionmaker(
    engine,
    class_ = AsyncSession,
    expire_on_commit = False,
)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


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
                title = post['title']
                description = post['body']
                user_id = post['userId']
                post = Post(title = title, description = description, user_id = user_id)
                session.add(post)


class User(Base):
    __tablename__ = 'user'


    id = Column(
        Integer,
        primary_key = True,
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
    created_at = Column(
        DateTime,
        nullable = False,
        default = datetime.utcnow,
        server_default = func.now(),
    )

    posts = relationship('Post', back_populates='users')

    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, name={self.name!r}, email={self.email},' \
               f'created_at={self.created_at!r})'


    def __repr__(self):
        return str(self)


class Post(Base):
    __tablename__ = 'posts'


    id = Column(
        Integer,
        primary_key = True,
    )
    title = Column(
        String,
        nullable='',
        default='',
        server_default='',
    )
    description = Column(
        String,
        nullable='',
        default='',
        server_default='',
    )
    user_id = Column(
        Integer,
        ForeignKey('user.id'),
        nullable = False,
    )

    users = relationship('User', back_populates='posts')


    def __str__(self):
        return f'{self.__class__.__name__}(id={self.id}, title={self.title!r}, description={self.description!r})'

    def __repr__(self):
        return str(self)