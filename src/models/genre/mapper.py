from src.models.genre.model import Genre
from src.models.genre.schema import GetGenreSchema


class GenreMapper:

    @staticmethod
    def from_model_to_schema(model: Genre) -> GetGenreSchema:
        return GetGenreSchema(
            id=model.id,
            name=model.name
        )
