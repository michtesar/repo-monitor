from typing import Any

from requests_cache import CachedSession
from repo_monitor.config import settings

from repo_monitor.utils import validate_github_url


class Repository:
    """
    Repository class as an interface to the
    cached events though GitHub API.
    """

    def __init__(self, url: str):
        """
        Class constructor
        :param url: GitHub repo url
        """
        validate_github_url(url)

        self._url = url
        self._api_url = self._create_api_url()

    def _create_api_url(self) -> str:
        """Construct API url from GitHub repo url"""
        *_, owner, repo = self._url.split("/")
        return f"https://api.github.com/repos/{owner}/{repo}/events"

    @property
    def url(self) -> str:
        return self._url

    # TODO: Implement better return model
    @property
    def events(self) -> list[dict[str, Any]]:
        """
        Lazy access to the repo events (cached)
        :return: List of events
        """
        with CachedSession(
            "events", expire_after=settings.cache_expiration_sec, backend="sqlite"
        ) as session:
            response = session.get(
                self._api_url, headers={"Accept": "application/vnd.github+json"}
            )
            if not response.ok:
                raise ValueError(f"Cannot retrieve events from: {self._api_url}: {response.text}")
            if not response.json():
                raise ValueError(f"Empty response from {self._api_url}")
        return response.json()  # type: ignore[no-any-return]
