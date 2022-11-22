from fastapi import FastAPI

from src import user, project

# Daniil Movchan
app = FastAPI(
    title='SBD Application',
    version="0.1.2",
)


app.include_router(user.user_endpoint, prefix="/api")
app.include_router(project.project_endpoint, prefix="/api")
