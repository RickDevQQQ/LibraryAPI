from typing import List

from fastapi import APIRouter, status

from src.core.database import SessionAnnotated
from src.models.book.schema import GetBookSchema, CreateBookSchema, PutBookSchema, Reservation
from src.models.book.service import BookService
from src.models.book.mapper import BookMapper
from src.models.genre.service import GenreService
from src.models.user.service import UserService

book_router = APIRouter(
    prefix='/book',
    tags=['Книги']
)


@book_router.post(
    '/',
    summary="Создать книгу",
    response_model=GetBookSchema,
    status_code=status.HTTP_201_CREATED
)
async def create(session: SessionAnnotated, schema: CreateBookSchema):
    book_service = BookService(
        session,
        GenreService(session),
        UserService(session)
    )
    book, genres = await book_service.create(schema)
    return BookMapper.from_model_to_schema(book, genres, None)


@book_router.get(
    '/',
    summary="Получить все книги",
    response_model=List[GetBookSchema]
)
async def get_all(
    session: SessionAnnotated
):
    book_service = BookService(
        session,
        GenreService(session),
        UserService(session)
    )
    response = []
    for book, genres in await book_service.get_all():
        reservation = await book_service.get_active_reservation(book.id)
        print(reservation)
        response.append(
            BookMapper.from_model_to_schema(book, genres, reservation)
        )
    return response


@book_router.get(
    '/{book_id}',
    summary="Получить кингу",
    response_model=GetBookSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {'message': 'Не найдена книга'}
    }
)
async def get(
    session: SessionAnnotated,
    book_id: int
):
    book_service = BookService(
        session,
        GenreService(session),
        UserService(session)
    )
    book, genres = await book_service.book_get_or_raise_by_id(book_id)
    reservation = await book_service.get_active_reservation(book.id)
    return BookMapper.from_model_to_schema(book, genres, reservation)


@book_router.put(
    '/{book_id}',
    summary="Изменить книгу",
    responses={
        status.HTTP_404_NOT_FOUND: {'message': 'Не найдена книга'}
    }
)
async def put(
    session: SessionAnnotated,
    schema: PutBookSchema,
    book_id: int
):
    book_service = BookService(
        session,
        GenreService(session),
        UserService(session)
    )
    book, genres = await book_service.put(book_id, schema)
    reservation = await book_service.get_active_reservation(book.id)
    return BookMapper.from_model_to_schema(book, genres, reservation)


@book_router.delete(
    '/{book_id}',
    summary="Удалить книгу",
    responses={
        status.HTTP_404_NOT_FOUND: {'message': 'Не найдена книга'}
    }
)
async def delete(session: SessionAnnotated, book_id: int):
    book_service = BookService(
        session,
        GenreService(session),
        UserService(session)
    )
    await book_service.delete(book_id)


@book_router.post(
    '/{book_id}/add-reservation',
    summary="Забронировать",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {'message': 'Не найдена книга'},
        status.HTTP_400_BAD_REQUEST: {
            'message': 'На книгу уже есть бронь в этот период. '
                       'Книга забронирована c {reservation.start_datetime} по {reservation.end_datetime}'
        }
    }
)
async def add_reservation(
    session: SessionAnnotated,
    schema: Reservation,
    book_id: int
):
    book_service = BookService(
        session,
        GenreService(session),
        UserService(session)
    )
    await book_service.add_reservation(
        book_id, start_datetime=schema.start_datetime, end_datetime=schema.end_datetime
    )
