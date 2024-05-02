from fastapi import FastAPI
from repo_monitor.config import settings
from repo_monitor.models.config import Config
from repo_monitor.models.events import Events
from repo_monitor.models.health import Health
from repo_monitor.models.repos import Repositories
from repo_monitor.models.stats import StatisticsSuccess, StatisticsFailed
from repo_monitor.repository import Repository
from repo_monitor.statistics import calculate_statistics

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


@app.post("/statistics")
async def post_statistics(
    repositories: Repositories,
) -> StatisticsSuccess | StatisticsFailed:
    repos = [Repository(r) for r in repositories.repositories]
    data = {}
    for repo in repos:
        data[repo.url] = [
            {
                "type": e.get("type"),
                "created_at": e.get("created_at"),
                "id": e.get("id"),
            }
            for e in repo.events
        ]
    try:
        statistics = calculate_statistics(data)
    except Exception as error:
        return StatisticsFailed(detail="Failed to calculate statistics", message=str(error))
    if statistics:
        return StatisticsSuccess(results=statistics)
    return StatisticsFailed(
        detail=f"Cannot calculate statistics for {[r.url for r in repos]}",
        message="Unknown error",
    )
