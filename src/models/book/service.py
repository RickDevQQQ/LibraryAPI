from datetime import datetime, UTC, timezone
from typing import List, Tuple, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload

from src.models import Book, Genre, BookGenre
from src.models.book.model import BookReservation
from src.models.book.schema import CreateBookSchema, PutBookSchema, GenreId
from src.models.genre.service import GenreService
from src.models.user.service import UserService


class BookService:

    def __init__(
        self,
        session: AsyncSession,
        genre_service: GenreService,
        user_service: UserService
    ) -> None:
        self.session = session
        self.genre_service = genre_service
        self.user_service = user_service

    async def check_reservation(
        self,
        book_id: int,
        start_datetime: datetime,
        end_datetime: datetime
    ) -> Optional[BookReservation]:
        return await BookReservation.get_models(
            self.session,
            filters=[  # type: ignore
                BookReservation.book_id == book_id,
                BookReservation.start_datetime < end_datetime,
                BookReservation.end_datetime > start_datetime
            ],
            first=True
        )

    async def get_active_reservation(self, book_id: int) -> List[BookReservation]:
        now = datetime.now()
        return await BookReservation.get_models(
            self.session,
            filters=[
                BookReservation.book_id == book_id,
                BookReservation.end_datetime > now
            ],
            order_by=BookReservation.end_datetime.desc()
        )

    async def add_reservation(self, book_id: int, start_datetime: datetime, end_datetime: datetime) -> None:
        book, genre = await self.book_get_or_raise_by_id(book_id)
        reservation = await self.check_reservation(book.id, start_datetime, end_datetime)
        if reservation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail={
                    'message': (
                        'На книгу уже есть бронь в этот период. '
                        f'Книга забронирована c {reservation.start_datetime} по {reservation.end_datetime}'
                    )
                }
            )
        reservation = BookReservation(
            book_id=book_id, start_datetime=start_datetime, end_datetime=end_datetime
        )
        self.session.add(reservation)
        await self.session.commit()

    async def book_get_or_raise_by_id(self, book_id: int) -> Tuple[Book, List[Genre]]:
        book = await Book.get_models(
            self.session, filters=[
                Book.id == book_id, Book.is_deleted.is_(False),
            ],
            load_options=[
                selectinload(Book.genres).options(
                    selectinload(BookGenre.genre)
                ),
                selectinload(Book.author)
            ],
            first=True
        )
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={
                    'message': 'Не найдена книга'
                }
            )
        genres = [item.genre for item in book.genres]
        return book, genres

    async def get_genres(self, book_id: int) -> List[Genre]:
        book_genres = await BookGenre.get_models(
            self.session,
            filters=[
                BookGenre.book_id == book_id
            ],
            load_options=[
                selectinload(BookGenre.genre)
            ]
        )
        return [item.genre for item in book_genres]

    async def put_book_genres(self, book_id: int, genres: List[GenreId]):
        genre_ids = [item.id for item in genres]
        created_genres = await self.get_genres(book_id)
        result = created_genres.copy()
        genres_data = {
            genre.id: genre
            for genre in await self.genre_service.genre_get_by_ids(genre_ids)
        }
        for item in genres:
            genre = genres_data.get(item.id)
            if not genre:
                continue

            if genre in created_genres:
                created_genres.remove(genre)
            else:
                result.append(genre)
                book_genre = BookGenre(book_id=book_id, genre_id=genre.id)
                self.session.add(book_genre)

        await BookGenre.delete(
            self.session,
            filters=[BookGenre.genre_id.in_([genre.id for genre in created_genres])]
        )
        return result

    async def create(self, schema: CreateBookSchema) -> Tuple[Book, List[Genre]]:
        author = await self.user_service.user_get_or_raise_by_id(schema.author_id)
        book = Book(
            name=schema.name,
            price=schema.price,
            page=schema.page,
            author=author
        )
        self.session.add(book)
        await self.session.flush()

        genres = await self.put_book_genres(book.id, schema.genres)
        await self.session.commit()
        return book, genres

    async def put(self, book_id: int, schema: PutBookSchema) -> Tuple[Book, List[Genre]]:
        author = await self.user_service.user_get_or_raise_by_id(schema.author_id)
        book, genres = await self.book_get_or_raise_by_id(book_id)
        book = await Book.update(
            self.session, filters=[Book.id == book.id], first=True,
            name=schema.name,
            price=schema.price,
            page=schema.page,
            author_id=author.id
        )
        book.author = author

        genres = await self.put_book_genres(book.id, schema.genres)
        await self.session.commit()
        return book, genres

    async def get_all(
        self
    ) -> List[Tuple[Book, List[Genre]]]:
        result = []
        filters = [Book.is_deleted.is_(False)]
        books = await Book.get_models(
            self.session, filters=filters, order_by=Book.id.desc(),
            load_options=[
                selectinload(Book.genres).options(
                    selectinload(BookGenre.genre)
                ),
                selectinload(Book.author)
            ]
        )
        for book in books:
            genres = [item.genre for item in book.genres]
            result.append((book, genres))
        return result

    async def delete(self, book_id: int) -> None:
        book, genres = await self.book_get_or_raise_by_id(book_id)
        book.is_deleted = True
        await self.session.commit()
