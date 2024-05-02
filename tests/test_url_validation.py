from unittest import TestCase

import pytest

from repo_monitor.lib.utils import validate_github_url


class TestGitHubURLValidation(TestCase):
    def test_valid_github_url(self) -> None:
        url = "https://github.com/username/repository"
        assert validate_github_url(url) is not None

    def test_invalid_url_scheme(self) -> None:
        url = "github.com/username/repository"
        with pytest.raises(ValueError):  # noqa: PT011
            validate_github_url(url)

    def test_non_github_url(self) -> None:
        url = "https://bitbucket.org/username/repository"
        with pytest.raises(ValueError):  # noqa: PT011
            validate_github_url(url)

    def test_empty_url(self) -> None:
        url = ""
        with pytest.raises(ValueError):  # noqa: PT011
            validate_github_url(url)

    def test_none_url(self) -> None:
        url = None
        with pytest.raises(ValueError):  # noqa: PT011
            validate_github_url(url)  # type: ignore[arg-type]
