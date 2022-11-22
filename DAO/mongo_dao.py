from datetime import datetime
from typing import List, Union

from bson import ObjectId
from pymongo import MongoClient

from DAO.idao import IDAO
from DAO.schemas.project import Project
from DAO.schemas.role import UserRoleEnum
from DAO.schemas.user import User, UserReg


class MongoDAO(IDAO):
    __conn: MongoClient = None
    __db = None

    def __init__(self):
        """CONNECT DB"""
        conn_str = "mongodb://localhost/sbdApp?retryWrites=true&w=majority"
        self.__conn = MongoClient('mongodb://localhost:27017/')
        self.__db = self.__conn.sbdApp

    # USER
    def get_users(self) -> List[User]:
        users = []

        for user in self.__db.user.find():
            users.append(User(**user))

        return users

    def get_user(self, email: str) -> User:
        user = self.__db.user.find_one({"email": email})
        if user:
            user = User(**user)
            return user
        else:
            return None

    def get_user_dict(self, email: str) -> dict:
        user = self.__db.user.find_one({"email": email})
        return user

    def save_user(self, user: UserReg) -> bool:
        try:
            user = user.dict()
            user['joined_at'] = datetime.now()
            self.__db.user.insert_one(user)
            return True
        except Exception:
            return False

    def save_user_dict(self, user: dict) -> bool:
        try:
            user['joined_at'] = datetime.now()
            self.__db.user.insert_one(user)
            return True
        except Exception:
            return False

    def update_user_role(self, email: str, pk_user_role: int) -> bool:
        try:
            role_name = UserRoleEnum(pk_user_role).name
            self.__db.user.update_one({'email': email},
                                      {'$set': {'user_role': role_name}},
                                      upsert=False)
            return True
        except Exception:
            return False

    def delete_user(self, pk_user: Union[str, int]) -> bool:
        try:
            self.__db.user.delete_one({'_id': ObjectId(pk_user)})
            return True
        except Exception:
            return False

    def delete_all_users(self):
        try:
            self.__db.user.delete_many({})
            return True
        except Exception:
            return False

    # PROJECT
    def get_projects(self) -> List[Project]:
        projects = []

        for project in self.__db.project.find():
            project['fk_user'] = str(project['fk_user'])
            projects.append(Project(**project))

        return projects

    def get_project(self, pk_project: Union[str, int]) -> Project:
        project = self.__db.project.find_one({"_id": ObjectId(pk_project)})
        if project:
            project['fk_user'] = str(project['fk_user'])
            project = Project(**project)
            return project
        else:
            return None

    def create_project(self, project: Project):
        try:
            project = project.dict()
            project['fk_user'] = ObjectId(project['fk_user'])
            project = self.__db.project.insert_one(project)
            return str(project.inserted_id)
        except Exception:
            return False

    def delete_project(self, pk_project: Union[int, str]) -> bool:
        try:
            self.__db.project.delete_one({'_id': ObjectId(pk_project)})
            return True
        except Exception:
            return False
