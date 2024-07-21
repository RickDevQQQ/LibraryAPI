from typing import Annotated
from pydantic import Field
from src.models.user.const import USER_FIELD_LAST_NAME_MAX_LENGTH, USER_FIELD_FIRST_NAME_MAX_LENGTH

UserIdFieldAnnotated = Annotated[
    int,
    Field(
        title="ИД автора",
        gt=0
    )
]
UserFirstNameFieldAnnotated = Annotated[
    str,
    Field(
        title="Имя",
        max_length=USER_FIELD_FIRST_NAME_MAX_LENGTH,
        min_length=1
    )
]
UserLastNameFieldAnnotated = Annotated[
    str,
    Field(
        title="Фамилия",
        max_length=USER_FIELD_LAST_NAME_MAX_LENGTH,
        min_length=1
    )
]
UserAvatarFieldAnnotated = Annotated[
    str,
    Field(
        title="Аватарка",
        min_length=1
    )
]

