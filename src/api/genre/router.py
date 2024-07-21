from fastapi import APIRouter

genre_router = APIRouter(
    prefix='/genre',
    tags=['Жанры']
)


@genre_router.post(
    '/',
    summary="Создать жанр"
)
async def create():
    ...


@genre_router.get(
    '/',
    summary="Получить все жанры"
)
async def get_all():
    ...


@genre_router.get(
    '/{genre_id}',
    summary="Получить определенный жанр"
)
async def get(genre_id: int):
    ...


@genre_router.put(
    '/{genre_id}',
    summary="Изменить жанр"
)
async def put(genre_id: int):
    ...


@genre_router.delete(
    '/{genre_id}',
    summary="Удалить жанр"
)
async def delete(genre_id: int):
    ...
