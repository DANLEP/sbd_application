from datetime import datetime
from typing import List, Union

from DAO.idao import IDAO
import pymysql.cursors

from DAO.schemas.user import User, UserReg


class MySQLDAO(IDAO):
    conn: pymysql.cursors = None

    GET_USERS = "SELECT `pk_user`, `email`, `password`, `joined_at`, `telegram_username`, `fk_user_role` FROM user;"
    GET_USER = "SELECT `pk_user`, `email`, `password`, `joined_at`, `telegram_username`, `fk_user_role` FROM user WHERE `email`=%s;"
    SAVE_USER = "INSERT INTO `user` (`email`, `password`, `joined_at`, `telegram_username`) VALUES (%s, %s, %s, %s);"
    UPDATE_USER_ROLE = "UPDATE `user` SET `fk_user_role`=%s WHERE `email`= %s;"
    DELETE_USER = "DELETE FROM `user` WHERE `pk_user`= %s;"
    DELETE_ALL_USER = "TRUNCATE `sbd_payment_gateway`.`user`;"

    def __init__(self):
        """CONNECT DB"""
        self.conn = pymysql.connect(host='localhost',
                                    user='root',
                                    password='Mnbvcxzaq789)',
                                    database='sbd_payment_gateway',
                                    cursorclass=pymysql.cursors.DictCursor)

    def get_user(self, email: str) -> User:
        with self.conn.cursor() as cursor:
            cursor.execute(self.GET_USER, (email,))
            result = cursor.fetchone()
            if result:
                return User(**result)
            else:
                return None

    def get_user_dict(self, email: str) -> dict:
        with self.conn.cursor() as cursor:
            cursor.execute(self.GET_USER, (email,))
            result = cursor.fetchone()
            return result

    def get_users(self) -> List[User]:
        users = []

        with self.conn.cursor() as cursor:
            cursor.execute(self.GET_USERS)
            result = cursor.fetchall()
            for res in result:
                user = User(**res)
                users.append(user)
        return users

    def save_user(self, user: UserReg) -> bool:
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(self.SAVE_USER, (user.email, user.password, datetime.now(), user.telegram_username))
                self.conn.commit()
                return True
        except Exception:
            return False

    def save_user_dict(self, user: dict) -> bool:
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(self.SAVE_USER,
                               (user['email'], user['password'], datetime.now(), user['telegram_username']))
                self.conn.commit()
                return True
        except Exception:
            return False

    def update_user_role(self, email: str, pk_user_role: Union[str, int]) -> bool:
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(self.UPDATE_USER_ROLE, (pk_user_role, email))
                self.conn.commit()
                return True
        except Exception:
            return False

    def delete_user(self, pk_user: Union[str, int]) -> bool:
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(self.DELETE_USER, (pk_user,))
                self.conn.commit()
                return True
        except Exception:
            return False

    def delete_all_users(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(self.DELETE_ALL_USER)
                self.conn.commit()
                return True
        except Exception:
            return False
