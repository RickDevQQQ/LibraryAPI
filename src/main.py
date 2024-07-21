from fastapi import FastAPI

from src.api.genre.router import genre_router
from src.api.user.router import user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(genre_router)

tag_healthcheck = 'healthcheck'


@app.get(
    '/health',
    tags=[tag_healthcheck],
    summary='Проверить работоспособность сервиса.'
)
async def health():
    return {'status': 'ok'}
