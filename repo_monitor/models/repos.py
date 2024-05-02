from pydantic import BaseModel, Field
from repo_monitor.config import settings


class Repositories(BaseModel):
    repositories: list[str] = Field(..., min_items=1, max_items=settings.max_repositories)
