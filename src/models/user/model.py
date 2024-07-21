from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import Model
from src.core.column import ColumnIdAutoIncrement
from src.models.user.const import (
    USER_FIELD_LAST_NAME_MAX_LENGTH,
    USER_FIELD_FIRST_NAME_MAX_LENGTH
)


class User(ColumnIdAutoIncrement, Model):
    first_name: Mapped[str] = mapped_column(
        String(USER_FIELD_FIRST_NAME_MAX_LENGTH), doc="Имя"
    )
    last_name: Mapped[str] = mapped_column(
        String(USER_FIELD_LAST_NAME_MAX_LENGTH), doc="Фамилия"
    )
    avatar: Mapped[str] = mapped_column(
        String, doc="Аватар"
    )
