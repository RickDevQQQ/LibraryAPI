from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status

from src.models.genre.model import Genre
from src.models.genre.schema import PutGenreSchema, CreateGenreSchema


class GenreService:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def genre_get_or_raise_by_id(self, genre_id: int) -> Genre:
        genre = await Genre.get_models(self.session, filters=[
            Genre.id == genre_id, Genre.is_deleted.is_(False)
        ], first=True)
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail={
                    'message': 'Не найден жанр'
                }
            )
        return genre

    async def create(self, schema: CreateGenreSchema) -> Genre:
        genre = Genre(name=schema.name)
        self.session.add(genre)
        await self.session.commit()
        return genre

    async def put(self, genre_id: int, schema: PutGenreSchema) -> Genre:
        genre = await self.genre_get_or_raise_by_id(genre_id)
        genre = await Genre.update(
            self.session, filters=[Genre.id == genre.id], first=True,
            name=schema.name
        )
        await self.session.commit()
        return genre

    async def get_all(
        self,
        filter_name: Optional[str] = None,
    ) -> List[Genre]:
        filters = [Genre.is_deleted.is_(False)]
        if filter_name:
            filters.append(Genre.name.ilike(f'%{filter_name}%'))
        return await Genre.get_models(
            self.session, filters=filters, order_by=Genre.id.desc()
        )

    async def delete(self, genre_id: int) -> None:
        genre = await self.genre_get_or_raise_by_id(genre_id)
        genre.is_deleted = True
        await self.session.commit()
