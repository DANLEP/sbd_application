import datetime

from pydantic import BaseModel


class UserRole(BaseModel):
    pk_user_role: int
    name: str


class UserBase(BaseModel):
    email: str


class UserLogin(UserBase):
    password: str


class UserReg(UserLogin):
    telegram_username: str


class User(UserReg):
    pk_user: int
    joined_at: datetime.datetime
    fk_user_role: int
