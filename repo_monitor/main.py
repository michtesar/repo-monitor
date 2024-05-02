from fastapi import FastAPI
from repo_monitor.config import settings
from repo_monitor.models.config import Config
from repo_monitor.models.events import Events
from repo_monitor.models.health import Health
from repo_monitor.models.repos import Repositories
from repo_monitor.models.stats import StatisticsSuccess, StatisticsFailed
from repo_monitor.lib.repository import Repository
from repo_monitor.lib.statistics import calculate_statistics

description = """
## RepoMonitor 🚀

Minimal API tool for monitoring GitHub statistics on repository events

### Functionality

Application allows user to:
1. View the GitHub repo events
2. Calculate statistics on all events or on filtered event

User can provide up to 5 GitHub repositories in the `repositories` key
of the JSON body alongside with the request.

For more, please read README.md
"""

tags_metadata = [
    {
        "name": "Processing",
        "description": "Read the GitHub repository events or calculate _minor_ statistics.",
    },
    {
        "name": "Monitoring",
        "description": "Utilities, such as config or health monitoring for the REST API.",
    },
]

app = FastAPI(
    title="RepoMonitor",
    description=description,
    summary="API for GitHub Events",
    version="0.1.0",
    contact={"name": "Michael Tesar", "email": "michtesar@gmail.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/license/mit"},
    tags_metadata=tags_metadata,
)


@app.get("/config", tags=["Monitoring"], name="App Configuration")
async def get_config() -> Config:
    """
    Show the current application configuration.
    """
    return Config(successful=True, results=settings)


@app.get("/health", tags=["Monitoring"], name="App Heath")
async def get_health() -> Health:
    """
    Endpoint that can be used for monitor the health of the application.
    """
    return Health(status=200, ready="OK")


@app.post("/events", tags=["Processing"], name="Events")
async def post_events(repositories: Repositories) -> Events:
    """
    Fetch the events from all requested repositories
    """
    repos = [Repository(r) for r in repositories.repositories]
    results = {}
    for repo in repos:
        results[repo.url] = repo.events
    return Events(successful=True, results=results, n_repos=len(results))


@app.post("/statistics", tags=["Processing"], name="Statistics")
async def post_statistics(
    repositories: Repositories, event_type: str | None = None
) -> StatisticsSuccess | StatisticsFailed:
    """
    Calculate the statistics for all (or filtered) events from all requested repositories
    """
    # Create repository objects from included strings
    repos = [Repository(r) for r in repositories.repositories]

    # Collect all events, ids and timestamps
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

    # Calculate statistics
    statistics = calculate_statistics(data, event_type)
    if statistics:
        return StatisticsSuccess(results=statistics)
    return StatisticsFailed(
        detail=f"Cannot calculate statistics for {[r.url for r in repos]}",
        message="Unknown error",
    )