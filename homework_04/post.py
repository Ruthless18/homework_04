from sqlalchemy import (
    Column,
    String,
    Integer,
)
from sqlalchemy.orm import relationship

from homework_04.models import Base
from homework_04.mixins import CreatedAtMixin


class Post(CreatedAtMixin, Base):
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