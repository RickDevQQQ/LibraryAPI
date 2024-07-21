from typing import List

from fastapi import APIRouter, status

from src.core.database import SessionAnnotated
from src.models.book.schema import GetBookSchema, CreateBookSchema, PutBookSchema
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
    return BookMapper.from_model_to_schema(book, genres)


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
    return [
        BookMapper.from_model_to_schema(book, genres)
        for book, genres in await book_service.get_all()
    ]


@book_router.get(
    '/{book_id}',
    summary="Получить кингу",
    response_model=GetBookSchema
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
    return BookMapper.from_model_to_schema(book, genres)


@book_router.put(
    '/{book_id}',
    summary="Изменить книгу"
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
    return BookMapper.from_model_to_schema(book, genres)


@book_router.delete(
    '/{book_id}',
    summary="Удалить книгу"
)
async def delete(session: SessionAnnotated, book_id: int):
    book_service = BookService(
        session,
        GenreService(session),
        UserService(session)
    )
    await book_service.delete(book_id)
