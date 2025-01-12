from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from .base import Base


class MixinAutoIdModel(Base):
    """
    Миксина для добавления автоинкрементного поля id.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
        autoincrement=True,
        comment='Идентификатор',
        sort_order=-10
    )
