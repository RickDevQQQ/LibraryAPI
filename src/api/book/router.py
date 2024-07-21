from fastapi import APIRouter

book_router = APIRouter(
    prefix='/book',
    tags=['Книги']
)


@book_router.post(
    '/',
    summary="Создать книгу"
)
async def create():
    ...


@book_router.get(
    '/',
    summary="Получить все книги"
)
async def get_all():
    ...


@book_router.get(
    '/{book_id}',
    summary="Получить определенную книгу"
)
async def get(book_id: int):
    ...


@book_router.put(
    '/{book_id}',
    summary="Изменить книгу"
)
async def put(book_id: int):
    ...


@book_router.delete(
    '/{book_id}',
    summary="Удалить книгу"
)
async def delete(book_id: int):
    ...
