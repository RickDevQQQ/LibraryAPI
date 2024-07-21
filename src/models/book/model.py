from decimal import Decimal

from sqlalchemy import String, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING, List

from src.core.column import ColumnIdAutoIncrement, ColumnIsDeleted
from src.core.model import Model
from src.models.book.const import BOOK_FIELD_NAME_MAX_LENGTH

if TYPE_CHECKING:
    from src.models.user.model import User
    from src.models.genre.model import Genre


class Book(ColumnIdAutoIncrement, ColumnIsDeleted, Model):
    name: Mapped[str] = mapped_column(
        String(BOOK_FIELD_NAME_MAX_LENGTH), doc="Наименование"
    )
    price: Mapped[Decimal] = mapped_column(
        DECIMAL(scale=2, precision=11, decimal_return_scale=2, asdecimal=True),
        doc="Стоимость"
    )
    page: Mapped[int] = mapped_column(
        Integer, doc="Количество страниц"
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('user.id', use_alter=True, onupdate="RESTRICT", ondelete="RESTRICT"),
        doc="ИД автора"
    )
    author: Mapped['User'] = relationship('User')
    genres: Mapped[List['BookGenre']] = relationship('BookGenre', back_populates='book')


class BookGenre(Model):
    book_id: Mapped[int] = mapped_column(
        ForeignKey('book.id', use_alter=True, onupdate="RESTRICT", ondelete="RESTRICT"),
        primary_key=True, doc="ИД книги"
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey('genre.id', use_alter=True, onupdate="RESTRICT", ondelete="RESTRICT"),
        primary_key=True, doc="ИД Жанра"
    )
    book: Mapped['Book'] = relationship('Book', back_populates='genres')
    genre: Mapped['Genre'] = relationship('Genre')
