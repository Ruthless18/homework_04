from sqlalchemy import (
    Column,
    String,
    Integer,
)
from sqlalchemy.orm import relationship

from homework_04.models import Base
from homework_04.mixins import CreatedAtMixin


class User(CreatedAtMixin, Base):
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

