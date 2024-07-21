from pydantic import BaseModel
from src.models.user.field import (
    UserIdFieldAnnotated,
    UserFirstNameFieldAnnotated,
    UserLastNameFieldAnnotated,
    UserAvatarFieldAnnotated
)


class CreateUserSchema(BaseModel):
    first_name: UserFirstNameFieldAnnotated
    last_name: UserLastNameFieldAnnotated
    avatar: UserAvatarFieldAnnotated


class PutUserSchema(CreateUserSchema):
    pass


class GetUserSchema(BaseModel):
    id: UserIdFieldAnnotated
    first_name: UserFirstNameFieldAnnotated
    last_name: UserLastNameFieldAnnotated
    avatar: UserAvatarFieldAnnotated
