from typing import List, Union

from DAO.schemas.user import User, UserReg


class IDAO:
    def get_users(self) -> List[User]:
        """GET ALL USERS"""
        pass

    def get_user(self, email: str) -> User:
        """GET USER BY EMAIL"""
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
