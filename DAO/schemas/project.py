import secrets
from datetime import datetime
from typing import Union

from bson import ObjectId
from pydantic import BaseModel

from DAO.schemas.project_status import ProjectStatusEnum


class ProjectBase(BaseModel):
    name: str
    description: str
    kind_of_activity: str
    fk_user: Union[str, int]


class Project(ProjectBase):
    pk_project: Union[str, int]
    created_at: datetime = datetime.now()
    fk_project_status: ProjectStatusEnum = ProjectStatusEnum.active
    project_status: str = ProjectStatusEnum.active.name
    api_key: str
    secret_key: str

    def __init__(self, **kwargs):
        if not kwargs.get('api_key'):
            kwargs['api_key'] = secrets.token_hex(32)
        if not kwargs.get('secret_key'):
            kwargs['secret_key'] = secrets.token_hex(16)

        if kwargs.get("_id"):
            kwargs['pk_project'] = str(kwargs['_id'])

        super(Project, self).__init__(**kwargs)
