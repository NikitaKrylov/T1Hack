from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime


class UserOutWithHashedPassword(UserOut):
    password: str


class UserCreate(BaseModel):
    email: EmailStr = Field(title='Это логин, но это почта')
    password: str

