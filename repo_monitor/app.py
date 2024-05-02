from fastapi import FastAPI
from repo_monitor.config import settings
from repo_monitor.models.config import Config
from repo_monitor.models.events import Events
from repo_monitor.models.health import Health
from repo_monitor.models.repos import Repositories
from repo_monitor.repository import Repository

app = FastAPI()


@app.get("/config")
async def get_config() -> Config:
    return Config(successful=True, results=settings)


@app.get("/health")
async def get_health() -> Health:
    return Health(status=200, ready="OK")


@app.post("/events")
async def post_events(repositories: Repositories) -> Events:
    repos = [Repository(r) for r in repositories.repositories]
    results = {}
    for repo in repos:
        results[repo.url] = repo.events
    return Events(successful=True, results=results, n_repos=len(results))
