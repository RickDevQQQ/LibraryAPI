from typing import List, Optional

from src.models import Book, Genre
from src.models.book.model import BookReservation
from src.models.book.schema import GetBookSchema, Reservation
from src.models.genre.mapper import GenreMapper
from src.models.user.mapper import UserMapper


class BookMapper:

    @staticmethod
    def from_model_to_schema(model: Book, genres: List[Genre], reservation: Optional[BookReservation]) -> GetBookSchema:
        return GetBookSchema(
            id=model.id,
            name=model.name,
            price=model.price,
            page=model.page,
            author=UserMapper.from_model_to_schema(model.author),
            genres=[
                GenreMapper.from_model_to_schema(genre)
                for genre in genres
            ],
            reservation=Reservation(
                start_datetime=reservation.start_datetime,
                end_datetime=reservation.end_datetime
            ) if reservation else None

        )
