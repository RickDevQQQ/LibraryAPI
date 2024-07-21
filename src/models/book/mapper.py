from typing import List

from src.models import Book, Genre
from src.models.book.schema import GetBookSchema
from src.models.genre.mapper import GenreMapper
from src.models.user.mapper import UserMapper


class BookMapper:

    @staticmethod
    def from_model_to_schema(model: Book, genres: List[Genre]) -> GetBookSchema:
        return GetBookSchema(
            id=model.id,
            name=model.name,
            price=model.price,
            page=model.page,
            author=UserMapper.from_model_to_schema(model.author),
            genres=[
                GenreMapper.from_model_to_schema(genre)
                for genre in genres
            ]

        )
