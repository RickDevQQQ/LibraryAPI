from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import Model
from src.core.column import ColumnIdAutoIncrement


class User(ColumnIdAutoIncrement, Model):
    first_name: Mapped[str] = mapped_column(
        String(255), doc="Имя"
    )
    last_name: Mapped[str] = mapped_column(
        String(255), doc="Фамилия"
    )
    avatar: Mapped[str] = mapped_column(
        String, doc="Аватар"
    )
