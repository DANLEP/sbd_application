from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel

from DAO.schemas.role import UserRoleEnum


class UserLogin(BaseModel):
    email: str
    password: str


class UserReg(UserLogin):
    telegram_username: str


class User(UserReg):
    pk_user: Union[int, str]
    joined_at: datetime = datetime.now()
    fk_user_role: UserRoleEnum = UserRoleEnum.merchant
    user_role: str

    def __init__(self, **kwargs):
        if kwargs.get("_id"):
            kwargs['pk_user'] = str(kwargs['_id'])
        if not kwargs.get("fk_user_role"):
            if not kwargs.get("user_role"):
                kwargs['fk_user_role'] = 1
            else:
                kwargs['fk_user_role'] = UserRoleEnum[kwargs['user_role']].value

        kwargs['user_role'] = UserRoleEnum(kwargs['fk_user_role']).name
        super(User, self).__init__(**kwargs)
