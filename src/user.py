from typing import Union

from fastapi import APIRouter
from starlette.responses import JSONResponse

from DAO.schemas.user import UserReg, UserLogin
from config import dao
from utils.password import Hasher

user_endpoint = APIRouter()


@user_endpoint.get("/users", tags=["user"])
async def get_all_users():
    users = dao.get_users()
    if users:
        return users
    else:
        return JSONResponse({"message": "User list empty"}, status_code=204)


@user_endpoint.get("/user", tags=["user"])
async def get_user(email: str):
    user = dao.get_user(email)
    if user:
        return user
    else:
        return JSONResponse({"message": "No such user"}, status_code=404)


@user_endpoint.post("/register", tags=["auth"])
async def register(user: UserReg):
    user.password = Hasher.get_password_hash(user.password)
    res = dao.save_user(user)
    if res:
        user = dao.get_user(user.email)
        return user
    else:
        return JSONResponse({"ok": res}, status_code=409)


@user_endpoint.post("/login", tags=["auth"])
async def login(user: UserLogin):
    user_db = await get_user(user.email)
    if Hasher.verify_password(user.password, user_db.password):
        user = user_db.dict(exclude={'password', 'telegram_username', 'joined_at'})
        return user
    else:
        return JSONResponse({"message": "Incorrect data"}, status_code=401)


@user_endpoint.put("/user/update_role", tags=["user"])
async def update_role(email: str, pk_user_role: int) -> JSONResponse:
    res = dao.update_user_role(email, pk_user_role)
    return JSONResponse({'ok': res})


@user_endpoint.delete("/user/{pk_user}", tags=["user"])
async def delete_user(pk_user: Union[int, str]) -> JSONResponse:
    res = dao.delete_user(pk_user)
    return JSONResponse({'ok': res})
