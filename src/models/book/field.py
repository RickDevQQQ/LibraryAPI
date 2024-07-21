from decimal import Decimal
from typing import Annotated
from pydantic import Field
from src.models.book.const import BOOK_FIELD_NAME_MAX_LENGTH

BookIdFieldAnnotated = Annotated[
    int,
    Field(
        title="ИД книги",
        gt=0
    )
]
BookNameFieldAnnotated = Annotated[
    str,
    Field(
        title="Наименование",
        max_length=BOOK_FIELD_NAME_MAX_LENGTH,
        min_length=1
    )
]
BookPriceFieldAnnotated = Annotated[
    Decimal,
    Field(
        title="Цена",
        gt=0
    )
]
BookPageFieldAnnotated = Annotated[
    int,
    Field(
        title="Количество страниц",
        gt=0
    )
]
