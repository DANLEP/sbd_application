from fastapi import APIRouter
from starlette.responses import JSONResponse

from DAO.schemas.project import Project, ProjectBase
from config import dao

project_endpoint = APIRouter()


@project_endpoint.get("/projects", tags=['project'])
async def get_projects():
    project = dao.get_projects()

    if project:
        return project
    else:
        return JSONResponse({"message": "Project list empty"}, status_code=204)


@project_endpoint.post("/project", tags=['project'])
async def create_project(project: ProjectBase):
    project = Project(**project.dict())

    res = dao.create_project(project)
    if res:
        project = dao.get_project(res)
        return project
    else:
        return JSONResponse({"ok": res}, status_code=409)


@project_endpoint.delete("/project/{pk_project}}", tags=['project'])
async def delete_project(pk_project) -> JSONResponse:
    res = dao.delete_project(pk_project)
    return JSONResponse({'ok': res})
