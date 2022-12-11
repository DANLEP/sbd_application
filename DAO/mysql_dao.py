from datetime import datetime
from pprint import pprint
from typing import List, Union

from DAO.idao import IDAO
import pymysql.cursors

from DAO.schemas.container import DBContainer
from DAO.schemas.project import Project
from DAO.schemas.user import User, UserReg


class MySQLDAO(IDAO):
    conn: pymysql.cursors = None

    GET_USERS = "SELECT `pk_user`, `email`, `password`, `joined_at`, `telegram_username`, `fk_user_role` FROM user;"
    GET_USER = "SELECT `pk_user`, `email`, `password`, `joined_at`, `telegram_username`, `fk_user_role` FROM user WHERE `email`=%s;"
    GET_USER_BY_PK = "SELECT `pk_user`, `email`, `password`, `joined_at`, `telegram_username`, `fk_user_role` FROM user WHERE `pk_user`=%s;"
    SAVE_USER = "INSERT INTO `user` (`email`, `password`, `joined_at`, `telegram_username`) VALUES (%s, %s, %s, %s);"
    UPDATE_USER_ROLE = "UPDATE `user` SET `fk_user_role`=%s WHERE `email`= %s;"
    DELETE_USER = "DELETE FROM `user` WHERE `pk_user`= %s;"
    DELETE_ALL_USER = "TRUNCATE `sbd_payment_gateway`.`user`;"

    GET_PROJECTS = "SELECT `pk_project`, `name`, `description`, `kind_of_activity`, `fk_user`, `created_at`, `fk_project_status`, `api_key`, `secret_key` FROM project;"
    SAVE_PROJECT = "INSERT INTO `sbd_payment_gateway`.`project` (`name`, `description`, `kind_of_activity`, `created_at`, `fk_user`, `fk_project_status`, `api_key`, `secret_key`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    DELETE_ALL_PROJECTS = "TRUNCATE `sbd_payment_gateway`.`project`;"
    FOREIGN_KEY_CHECKS = "SET FOREIGN_KEY_CHECKS = %s;"

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

    def get_user_by_pk(self, pk: Union[str, int]) -> User:
        with self.conn.cursor() as cursor:
            cursor.execute(self.GET_USER_BY_PK, (pk,))
            result = cursor.fetchone()
            if result:
                return User(**result)
            else:
                return None

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

    def get_projects(self) -> List[Project]:
        projects = []

        with self.conn.cursor() as cursor:
            cursor.execute(self.GET_PROJECTS)
            result = cursor.fetchall()
            for res in result:
                project = Project(**res)
                projects.append(project)
        return projects

    def create_project(self, project: Project):
        fk_user = project.fk_user
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(self.SAVE_PROJECT, (project.name, project.description, project.kind_of_activity,
                                                   project.created_at, project.fk_user, project.fk_project_status.value,
                                                   project.api_key, project.secret_key))
                self.conn.commit()
                return True
        except Exception as e:
            pprint(e)
            return False

    def export_data(self) -> DBContainer:
        try:
            users = self.get_users()
            projects = self.get_projects()
            return DBContainer(users=users, projects=projects)
        except Exception:
            return None

    def import_data(self, data: DBContainer) -> bool:
        try:
            users = data.users
            for user in users:
                self.save_user(user)

            projects = data.projects
            for project in projects:
                self.create_project(project)
            return True
        except Exception:
            return False

    def migrate_project_keys(self, projects: List[Project]):
        new_projects = []
        try:
            for project in projects:
                user = self.get_user_by_pk(project.fk_user)
                project.fk_user = user.pk_user
                new_projects.append(project)
            return new_projects
        except Exception as e:
            return None

    def drop_db(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(self.FOREIGN_KEY_CHECKS, (0,))

                cursor.execute(self.DELETE_ALL_PROJECTS)
                cursor.execute(self.DELETE_ALL_USER)

                cursor.execute(self.FOREIGN_KEY_CHECKS, (1,))
                self.conn.commit()
                return True
        except Exception as e:
            pprint(e)
            return False