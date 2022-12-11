from typing import List, Optional

from pydantic import BaseModel

from DAO.schemas.project import Project
from DAO.schemas.user import User


class DBContainer(BaseModel):
    users: Optional[List[User]] = []
    projects: Optional[List[Project]] = []
