from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.model import Model
from src.core.column import ColumnIdAutoIncrement, ColumnIsDeleted
from src.models.genre.const import GENRE_FIELD_NAME_MAX_LENGTH


class Genre(ColumnIdAutoIncrement, ColumnIsDeleted, Model):
    name: Mapped[str] = mapped_column(
        String(GENRE_FIELD_NAME_MAX_LENGTH), doc="Имя"
    )
