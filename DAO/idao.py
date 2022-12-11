from typing import List, Union

from DAO.schemas.container import DBContainer
from DAO.schemas.project import Project
from DAO.schemas.user import User, UserReg


class IDAO:
    def get_users(self) -> List[User]:
        """GET ALL USERS"""
        pass

    def get_user(self, email: str) -> User:
        """GET USER BY EMAIL"""
        pass

    def get_user_by_pk(self, pk: Union[str, int]) -> User:
        """GET USER BY PK"""
        pass

    def get_user_dict(self, email: str) -> dict:
        """GET USER BY EMAIL"""
        pass

    def save_user(self, user: UserReg) -> bool:
        """SAVE USER"""
        pass

    def save_user_dict(self, user: dict) -> bool:
        """SAVE USER DICT"""
        pass

    def update_user_role(self, email: str, pk_user_role: Union[str, int]) -> bool:
        """UPDATE USER ROLE"""
        pass

    def delete_user(self, pk_user: Union[str, int]) -> bool:
        """DELETE USER"""
        pass

    def get_projects(self) -> List[Project]:
        """GET ALL PROJECTS"""
        pass

    def create_project(self, project: Project):
        """CREATE PROJECT"""
        pass

    def migrate_project_keys(self, projects: List[Project]):
        """"""
        pass

    def export_data(self) -> DBContainer:
        """EXPORT ALL DATA"""
        pass

    def import_data(self, data: DBContainer) -> bool:
        """IMPORT ALL DATA"""
        pass

    def drop_db(self):
        """DROP ALL DB DATA"""
        pass
