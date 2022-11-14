from typing import List

from fastapi import FastAPI

from DAO.dao_factory import DAOFactory
from DAO.schemas.user import User, UserReg, UserLogin
from DAO.type_dao import TypeDAO
from utils.password import Hasher

app = FastAPI()
dao = DAOFactory.get_dao_instance(TypeDAO.MySQL)


# Daniil Movchan
@app.get("/api/users")
async def get_all_users() -> List[User]:
    return dao.get_users()


@app.get("/api/user")
async def get_user(email: str) -> User:
    return dao.get_user(email)


@app.post("/api/register")
async def register(user: UserReg) -> bool:
    user.password = Hasher.get_password_hash(user.password)
    return dao.save_user(user)


@app.post("/api/login")
async def login(user: UserLogin) -> dict:
    user_db = await get_user(user.email)
    if Hasher.verify_password(user.password, user_db.password):
        return user_db.dict(exclude={'password', 'telegram_username', 'joined_at'})
    else:
        return {"message": "Incorrect data"}


@app.put("/api/user/update_role")
async def update_role(email: str, pk_user_role: int) -> bool:
    return dao.update_user_role(email, pk_user_role)


@app.delete("/api/user/{pk_user}/delete")
async def delete_user(pk_user: int) -> bool:
    return dao.delete_user(pk_user)
