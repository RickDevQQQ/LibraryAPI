from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from src.models.book.field import (
    BookIdFieldAnnotated,
    BookNameFieldAnnotated,
    BookPageFieldAnnotated,
    BookPriceFieldAnnotated
)
from src.models.user.field import UserIdFieldAnnotated
from src.models.user.schema import GetUserSchema

from src.models.genre.field import GenreIdFieldAnnotated
from src.models.genre.schema import GetGenreSchema


class GenreId(BaseModel):
    id: GenreIdFieldAnnotated


class CreateBookSchema(BaseModel):
    name: BookNameFieldAnnotated
    page: BookPageFieldAnnotated
    price: BookPriceFieldAnnotated
    author_id: UserIdFieldAnnotated
    genres: List[GenreId]


class PutBookSchema(CreateBookSchema):
    pass


class Reservation(BaseModel):
    start_datetime: datetime
    end_datetime: datetime


class GetBookSchema(BaseModel):
    id: BookIdFieldAnnotated
    name: BookNameFieldAnnotated
    page: BookPageFieldAnnotated
    price: BookPriceFieldAnnotated
    author: GetUserSchema
    genres: List[GetGenreSchema]
    reservation: List[Reservation]
