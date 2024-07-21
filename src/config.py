from pydantic_settings import BaseSettings


class ApplicationConfig(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    ECHO: bool

    @property
    def default_asyncpg_url(self) -> str:
        return "postgresql+asyncpg://postgres:example@db/library"


app_config = ApplicationConfig()
