from datetime import datetime
from pprint import pprint
from typing import List, Union

from bson import ObjectId
from pymongo import MongoClient

from DAO.idao import IDAO
from DAO.schemas.container import DBContainer
from DAO.schemas.project import Project
from DAO.schemas.role import UserRoleEnum
from DAO.schemas.user import User, UserReg


class MongoDAO(IDAO):
    __conn: MongoClient = None
    __db = None

    def __init__(self,
                 conn_str='mongodb://localhost:27017/'
                 ):
        """CONNECT DB"""
        self.__conn = MongoClient(conn_str)
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

    def get_user_by_pk(self, pk_user: int) -> User:
        user = self.__db.user.find_one({"pk_user": int(pk_user)})
        if user:
            user = User(**user)
            return user
        else:
            return None

    def get_user_by_id(self, id: str) -> User:
        user = self.__db.user.find_one({"_id": ObjectId(id)})
        if user:
            user = User(**user)
            return user
        else:
            return None

    def get_user_dict(self, email: str, r_concern=None) -> dict:
        if r_concern:
            user = self.__db.user.with_options(read_concern=r_concern).find_one({"email": email})
        else:
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

    def save_user_dict(self, user: dict, w_concern = None) -> bool:
        try:
            user['joined_at'] = datetime.now()
            if w_concern:
                self.__db.user.with_options(write_concern=w_concern).insert_one(user)
            else:
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

    def export_data(self) -> DBContainer:
        try:
            users = self.get_users()
            projects = self.get_projects()

            new_projects = []
            for project in projects:
                user = self.__db.user.find_one({"_id": ObjectId(project.fk_user)})
                project.fk_user = int(user['pk_user'])
                new_projects.append(project)

            return DBContainer(users=users, projects=projects)
        except Exception as e:
            pprint(e)
            return None

    def import_data(self, data: DBContainer) -> bool:
        try:
            users = data.users
            for user in users:
                self.save_user_dict(user.dict())

            projects = self.migrate_project_keys(data.projects)
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
        except Exception:
            return None

    def drop_db(self):
        try:
            self.__db.user.delete_many({})
            self.__db.project.delete_many({})
            return True
        except Exception:
            return False
