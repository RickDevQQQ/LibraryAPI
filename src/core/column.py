from decimal import Decimal

from sqlalchemy import false, Boolean, text, BigInteger, Integer, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from typing import Annotated
import datetime as dt

CurrencyAnnotated = Annotated[
    Mapped[Decimal],
    mapped_column(
        DECIMAL(scale=2, precision=11, decimal_return_scale=2, asdecimal=True),
        doc="Стоимость"
    )
]


class ColumnIsDeleted:
    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        doc="Является удаленным"
    )


class ColumnUpdatedAt:
    created_at: Mapped[dt.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=dt.datetime.now(dt.UTC),
        doc="Время обновления"
    )


class ColumnCreatedAt:
    updated_at: Mapped[dt.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        doc="Время создания"
    )


class ColumnIdAutoIncrement:
    id: Mapped[BigInteger] = mapped_column(
        Integer, primary_key=True, autoincrement=True, doc="ИД записи"
    )
