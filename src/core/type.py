from typing import TypeAlias, Union

from sqlalchemy import BinaryExpression

DBFilterType: TypeAlias = Union[bool, BinaryExpression]