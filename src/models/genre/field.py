from decimal import Decimal
from typing import Annotated
from pydantic import Field
from src.models.genre.const import GENRE_FIELD_NAME_MAX_LENGTH

GenreIdFieldAnnotated = Annotated[
    int,
    Field(
        title="ИД жанра",
        gt=0
    )
]
GenreNameFieldAnnotated = Annotated[
    str,
    Field(
        title="Наименование",
        max_length=GENRE_FIELD_NAME_MAX_LENGTH,
        min_length=1
    )
]
