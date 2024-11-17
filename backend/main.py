from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.routers.users import router as users_router
from src.routers.sprints import router as sprints_router
from src.routers.entities import router as entities_router
from src.routers.history import router as history_router
from src.routers.metrix import router as metrix_router
from src.params.config import config
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(root_path='/api' if config.is_prod else '', lifespan=lifespan)


origins = [
    'http://localhost',
    'http://localhost:8080',
    'http://localhost:3000',
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(users_router)
app.include_router(sprints_router)
app.include_router(entities_router)
app.include_router(history_router)
app.include_router(metrix_router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
