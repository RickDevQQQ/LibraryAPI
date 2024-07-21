from fastapi import FastAPI

app = FastAPI()

tag_healthcheck = 'healthcheck'


@app.get(
    '/health',
    tags=[tag_healthcheck],
    summary='Проверить работоспособность сервиса.'
)
async def health():
    return {'status': 'ok'}
