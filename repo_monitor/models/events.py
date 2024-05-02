from typing import Any

from pydantic import BaseModel


class Events(BaseModel):
    successful: bool
    results: dict[str, Any]
    n_repos: int
