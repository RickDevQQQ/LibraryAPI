from pydantic import BaseModel
from src.models.genre.field import GenreIdFieldAnnotated, GenreNameFieldAnnotated


class CreateGenreSchema(BaseModel):
    name: GenreNameFieldAnnotated


class PutGenreSchema(CreateGenreSchema):
    pass


class GetGenreSchema(BaseModel):
    id: GenreIdFieldAnnotated
    name: GenreNameFieldAnnotated

