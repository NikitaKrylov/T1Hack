from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from src.params.config import config


SECRET_KEY = 'bouvgprvywgV68WEV68WEGVWE8Vw86egfw76EV6w7ve7'
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/users/login' if config.is_prod else '/users/login')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

