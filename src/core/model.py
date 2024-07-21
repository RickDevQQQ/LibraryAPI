from sqlalchemy import MetaData, select, ColumnElement, update
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr

from typing import Optional, List, Self, Dict, Union

from src.core.type import DBFilterType

__all__ = (
    "Model",
)

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(table_name)s_%(column_0_N_name)s ",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s ",
        "ck": "ck_%(table_name)s_%(constraint_name)s ",
        "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class Model(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    metadata = metadata

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

    @classmethod
    @declared_attr
    def __tablename__(cls) -> str:
        result = ""
        for item in cls.__name__:
            if item.isupper():
                result += "_"
            result += item
        return result[1:].lower()

    @classmethod
    async def get_models(
        cls,
        session: AsyncSession,
        filters: List[DBFilterType],
        load_options: Optional[List] = None,
        joins: Optional[List] = None,
        order_by: Optional[ColumnElement] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        first: bool = False
    ) -> Union[List[Self] | Self]:
        query = select(cls)
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        if joins:
            for join_model, on_clause in joins:
                if on_clause is not None:
                    query = query.join(join_model, on_clause)
                else:
                    query = query.join(join_model)
        if filters:
            query = query.filter(*filters)
        if load_options:
            for option in load_options:
                query = query.options(option)

        query = query.order_by(order_by)
        result = await session.execute(query)
        if first:
            return result.scalars().first()
        return list(result.scalars().all())

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        filters: List[bool],
        **kwargs
    ) -> List[Self]:
        query = (
            update(cls)
            .filter(*filters)
            .values(**kwargs)
            .returning(cls)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        """Создаёт объект из словаря."""
        return cls(**data)

    def to_dict(self) -> Dict:
        """Преобразует объект в словарь."""
        return {c.key: getattr(self, c.key) for c in getattr(self.__table__, "columns", [])}
