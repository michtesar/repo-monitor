from unittest import TestCase

import pytest

from repo_monitor.lib.repository import Repository


class TestRepositoryMethods(TestCase):
    def test_api_url_valid(self) -> None:
        repo = Repository("https://github.com/repos/username/repo")
        assert repo._api_url == "https://api.github.com/repos/username/repo/events"

    def test_api_url_invalid(self) -> None:
        with pytest.raises(ValueError):  # noqa: PT011
            Repository("https://gitlab.com/repos/username/repo")
