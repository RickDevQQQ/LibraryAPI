from fastapi import APIRouter

user_router = APIRouter(
    prefix='/user',
    tags=['Авторы']
)


@user_router.post(
    '/',
    summary="Создать автора"
)
async def create():
    ...


@user_router.get(
    '/',
    summary="Получить всех авторов"
)
async def get_all():
    ...


@user_router.get(
    '/{user_id}',
    summary="Получить определенного автора"
)
async def get(user_id: int):
    ...


@user_router.put(
    '/{user_id}',
    summary="Изменить автора"
)
async def put(user_id: int):
    ...


@user_router.delete(
    '/{user_id}',
    summary="Удалить автора"
)
async def delete(user_id: int):
    ...
