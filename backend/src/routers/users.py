from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.users import UserCreate, UserOut, Token
from src.services.users import get_current_user
from src.services import users as service

router = APIRouter(
    prefix="/users",
    tags=['Пользователи']
)


@router.get('', response_model=list[UserOut])
async def get_users_list():
    return await service.get_users_list()


@router.post('/login', response_model=Token)
async def authenticate_user(login_form: OAuth2PasswordRequestForm = Depends()):
    return await service.login_user(login_form.username, login_form.password)


@router.post('/register', response_model=UserOut)
async def register_user(user: UserCreate):
    return await service.register_user(user)


@router.get('/me', response_model=UserOut)
async def get_current_auth_user(current_user: UserOut = Depends(get_current_user)):
    return current_user


@router.get('/{user_id}', response_model=UserOut, dependencies=[Depends(get_current_user)])
async def get_user(user_id: int):
    return await service.get_user_by_id(user_id)


@router.delete('/{user_id}')
async def delete_user(user_id: int):
    await service.delete_users(user_id)

