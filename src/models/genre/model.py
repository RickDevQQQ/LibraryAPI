from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, TYPE_CHECKING

from src.core.model import Model
from src.core.column import ColumnIdAutoIncrement
from src.models.genre.const import GENRE_FIELD_NAME_MAX_LENGTH

if TYPE_CHECKING:
    from src.models.book.model import Book


class Genre(ColumnIdAutoIncrement, Model):
    name: Mapped[str] = mapped_column(
        String(GENRE_FIELD_NAME_MAX_LENGTH), doc="Имя"
    )
    books: Mapped[List['Book']] = relationship(
        'Book',
        secondary='BookGenre',
        back_populates='genres'
    )
