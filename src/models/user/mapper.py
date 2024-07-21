from src.models import User
from src.models.user.schema import GetUserSchema


class UserMapper:

    @staticmethod
    def from_model_to_schema(model: User) -> GetUserSchema:
        return GetUserSchema(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            avatar=model.avatar
        )
