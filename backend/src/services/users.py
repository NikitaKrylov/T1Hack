from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import HTTPException, status, Depends
import src.params.auth as auth
from src.database.db import async_session
from src.database.models import User
from src.schemas.users import UserOut, UserCreate
from src.database.cruds import users


def hash_password(password: str) -> str:
    return auth.pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return auth.pwd_context.verify(plain_password, hashed_password)


async def auth_user(email: str, password: str) -> UserOut:
    async with async_session() as session:
        user = await users.get_by_login(session, email)
        if not user:
            raise HTTPException(
                detail='Пользователь не найден. Проверьте почту или пароль',
                status_code=status.HTTP_400_BAD_REQUEST
            )

        if not verify_password(password, user.password):
            raise HTTPException(
                detail='Пользователь не найден. Проверьте почту или пароль',
                status_code=status.HTTP_400_BAD_REQUEST
            )

        return user


async def login_user(email: str, password: str):
    user = await auth_user(email, password)
    access_token = await create_access_token({'user_id': user.id})

    user_data = {
        'access_token': access_token,
        'token_type': 'bearer'
    }

    return user_data


async def register_user(user: UserCreate) -> UserOut:
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    async with async_session() as session:
        existed_user = await base_db.get_by(session, User, (User.email == user.email), UserOut)
        if existed_user:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Пользователь с таким логином уже существует')
        return await base_db.create_one(session, User, user, UserOut)


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(days=7)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        auth.SECRET_KEY,
        algorithm=auth.ALGORITHM
    )
    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> int:
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        now = datetime.now()
        exp = datetime.fromtimestamp(payload.get('exp'))

        if now > exp:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Время сессии истекло.')

    except ExpiredSignatureError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Время сессии истекло.')

    except JWTError:
        raise credentials_exception

    return user_id


async def get_current_user(token: str = Depends(auth.oauth2_scheme)) -> UserOut:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Не получилось авторизироваться в системе",
                                          headers={"WWW-Authenticate": "Bearer"})

    user_id = verify_access_token(token, credentials_exception)

    async with async_session() as session:
        user = await base_db.get_one_or_none_by_id(session, User, user_id, UserOut)

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return user


async def get_users_list() -> list[UserOut]:
    async with async_session() as session:
        return await base_db.get_all(session, User, UserOut)


async def get_user_by_id(user_id: int) -> UserOut | None:
    async with async_session() as session:
        return await base_db.get_one_or_none_by_id(session, User, user_id, UserOut)


async def delete_users(user_id: int) -> None:
    async with async_session() as session:
        await base_db.delete_by_id(session, User, user_id)

