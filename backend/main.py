import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.routers.users import router as users_router
from src.routers.sprints import router as sprints_router
from src.routers.entities import router as entities_router
from src.routers.history import router as history_router
from src.params.config import config


app = FastAPI(root_path='/api' if config.is_prod else '')


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

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
