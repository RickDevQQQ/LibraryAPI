from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from src.models.user.model import User
from src.models.user.schema import PutUserSchema, CreateUserSchema


class UserService:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def user_get_or_raise_by_id(self, user_id) -> User:
        user = await User.get_models(self.session, filters=[
            User.id == user_id, User.is_deleted.is_(False)
        ], first=True)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={
                    'message': 'Не найден пользователь'
                }
            )
        return user

    async def create(self, schema: CreateUserSchema) -> User:
        user = User(
            first_name=schema.first_name,
            last_name=schema.last_name,
            avatar=schema.avatar
        )
        self.session.add(user)
        await self.session.commit()
        return user

    async def put(self, user_id: int, schema: PutUserSchema) -> User:
        user = await self.user_get_or_raise_by_id(user_id)
        user = await User.update(
            self.session, filters=[User.id == user.id], first=True,
            first_name=schema.first_name,
            last_name=schema.last_name,
            avatar=schema.avatar,
        )
        await self.session.commit()
        return user

    async def get_all(
        self,
        filter_first_name: Optional[str] = None,
        filter_last_name: Optional[str] = None,
    ) -> List[User]:
        filters = [User.is_deleted.is_(False)]
        if filter_first_name:
            filters.append(User.first_name.ilike(f'%{filter_first_name}%'))
        if filter_last_name:
            filters.append(User.last_name.ilike(f'%{filter_last_name}%'))
        return await User.get_models(
            self.session, filters=filters, order_by=User.id.desc()
        )

    async def delete(self, user_id: int) -> None:
        user = await self.user_get_or_raise_by_id(user_id)
        user.is_deleted = True
        await self.session.commit()
