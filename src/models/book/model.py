from decimal import Decimal

from sqlalchemy import String, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING, List

from src.core.column import ColumnIdAutoIncrement
from src.core.model import Model

if TYPE_CHECKING:
    from src.models.user.model import User
    from src.models.genre.model import Genre


class Book(ColumnIdAutoIncrement, Model):
    name: Mapped[str] = mapped_column(
        String(255), doc="Наименование"
    )
    price: Mapped[Decimal] = mapped_column(
        DECIMAL(scale=2, precision=11, decimal_return_scale=2, asdecimal=True),
        doc="Стоимость"
    )
    page: Mapped[int] = mapped_column(
        Integer, doc="Количество страниц"
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('author.id', use_alter=True, onupdate="RESTRICT", ondelete="RESTRICT"),
        doc="ИД автора"
    )
    author: Mapped['User'] = relationship('User')

    genres: Mapped[List['Genre']] = relationship(
        'Genre',
        secondary='BookGenre',
        back_populates='books'
    )


class BookGenre(Model):
    book_id: Mapped[int] = mapped_column(
        ForeignKey('book.id', use_alter=True, onupdate="RESTRICT", ondelete="RESTRICT"),
        primary_key=True, doc="ИД книги"
    )
    genre_id: Mapped[int] = mapped_column(
        ForeignKey('genre.id', use_alter=True, onupdate="RESTRICT", ondelete="RESTRICT"),
        primary_key=True, doc="ИД Жанра"
    )
