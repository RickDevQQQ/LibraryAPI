from typing import List, Optional

from fastapi import APIRouter, status

from src.core.database import SessionAnnotated
from src.models.user.mapper import UserMapper
from src.models.user.schema import CreateUserSchema, GetUserSchema, PutUserSchema
from src.models.user.service import UserService

user_router = APIRouter(
    prefix='/user',
    tags=['Авторы']
)


@user_router.post(
    '/',
    summary="Создать автора",
    response_model=GetUserSchema,
    status_code=status.HTTP_201_CREATED
)
async def create(session: SessionAnnotated, schema: CreateUserSchema):
    user_service = UserService(session)
    user = await user_service.create(schema)
    return UserMapper.from_model_to_schema(user)


@user_router.get(
    '/',
    summary="Получить всех авторов",
    response_model=List[GetUserSchema]
)
async def get_all(
    session: SessionAnnotated,
    filter_first_name: Optional[str] = None,
    filter_last_name: Optional[str] = None,
):
    user_service = UserService(session)
    return [
        UserMapper.from_model_to_schema(user)
        for user in await user_service.get_all(
            filter_first_name=filter_first_name,
            filter_last_name=filter_last_name
        )
    ]


@user_router.get(
    '/{user_id}',
    summary="Получить определенного автора",
    response_model=GetUserSchema
)
async def get(session: SessionAnnotated, user_id: int):
    user_service = UserService(session)
    user = await user_service.user_get_or_raise_by_id(user_id)
    return UserMapper.from_model_to_schema(user)


@user_router.put(
    '/{user_id}',
    summary="Изменить автора",
    response_model=GetUserSchema,
    responses={
        status.HTTP_404_NOT_FOUND: {"message": "Не найден пользователь"}
    }
)
async def put(session: SessionAnnotated, schema: PutUserSchema, user_id: int):
    user_service = UserService(session)
    user = await user_service.put(user_id, schema)
    return UserMapper.from_model_to_schema(user)


@user_router.delete(
    '/{user_id}',
    summary="Удалить автора",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(session: SessionAnnotated, user_id: int):
    user_service = UserService(session)
    await user_service.delete(user_id)


