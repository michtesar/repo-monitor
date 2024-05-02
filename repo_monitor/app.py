from fastapi import FastAPI
from repo_monitor.config import settings
from repo_monitor.models.repos import Repositories
from repo_monitor.repository import Repository

app = FastAPI()


@app.get("/config")
async def get_config() -> dict[str, dict]:
    return {"results": settings.dict()}


@app.post("/events")
async def get_events(repositories: Repositories) -> dict:
    repos = [Repository(r) for r in repositories.repositories]
    result = {}
    for repo in repos:
        result[repo.url] = repo.events
    return {"results": result}
