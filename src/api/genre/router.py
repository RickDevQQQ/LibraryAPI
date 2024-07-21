from typing import List, Optional

from fastapi import APIRouter, status
from src.core.database import SessionAnnotated
from src.models.genre.mapper import GenreMapper
from src.models.genre.schema import CreateGenreSchema, GetGenreSchema, PutGenreSchema
from src.models.genre.service import GenreService

genre_router = APIRouter(
    prefix='/genre',
    tags=['Жанры']
)


@genre_router.post(
    '/',
    summary="Создать жанр",
    status_code=status.HTTP_201_CREATED,
    response_model=GetGenreSchema
)
async def create(session: SessionAnnotated, schema: CreateGenreSchema):
    genre_service = GenreService(session)
    genre = await genre_service.create(schema)
    return GenreMapper.from_model_to_schema(genre)


@genre_router.get(
    '/',
    summary="Получить все жанры",
    response_model=List[GetGenreSchema]
)
async def get_all(session: SessionAnnotated, filter_name: Optional[str] = None):
    genre_service = GenreService(session)
    return [
        GenreMapper.from_model_to_schema(genre)
        for genre in await genre_service.get_all(filter_name)
    ]


@genre_router.get(
    '/{genre_id}',
    summary="Получить определенный жанр",
    responses={
        status.HTTP_404_NOT_FOUND: {'message': 'Не найден жанр'}
    }
)
async def get(session: SessionAnnotated, genre_id: int):
    genre_service = GenreService(session)
    genre = await genre_service.genre_get_or_raise_by_id(genre_id)
    return GenreMapper.from_model_to_schema(genre)


@genre_router.put(
    '/{genre_id}',
    summary="Изменить жанр",
    responses={
        status.HTTP_404_NOT_FOUND: {'message': 'Не найден жанр'}
    }
)
async def put(session: SessionAnnotated, schema: PutGenreSchema, genre_id: int):
    genre_service = GenreService(session)
    genre = await genre_service.put(genre_id, schema)
    return GenreMapper.from_model_to_schema(genre)


@genre_router.delete(
    '/{genre_id}',
    summary="Удалить жанр",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: {'message': 'Не найден жанр'}
    }
)
async def delete(session: SessionAnnotated, genre_id: int):
    genre_service = GenreService(session)
    await genre_service.delete(genre_id)
