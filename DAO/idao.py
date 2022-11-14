from typing import List

from DAO.schemas.user import User


class IDAO:
    def get_users(self) -> List[User]:
        """GET ALL USERS"""
        pass

    def get_user(self, email: str) -> User:
        """GET USER BY EMAIL"""
        pass

    def save_user(self, user: User) -> User:
        """SAVE USER"""
        pass

    def update_user_role(self, pk_user_role: int) -> User:
        """UPDATE USER ROLE"""
        pass

    def delete_user(self, pk_user: int) -> bool:
        """DELETE USER"""
        pass
