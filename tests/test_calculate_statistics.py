from typing import Any
from unittest import TestCase

from repo_monitor.lib.statistics import calculate_statistics


class TestCalculateStatistics(TestCase):
    def test_calculate_statistics_no_event_type(self) -> None:
        repo_events = {
            "https://github.com/user/repo": [
                {"type": "PushEvent", "created_at": "2023-05-01T12:00:00Z"},
                {"type": "PullRequestEvent", "created_at": "2023-05-01T12:01:00Z"},
            ]
        }
        result = calculate_statistics(repo_events)
        assert result is not None
        assert result.repository == "https://github.com/user/repo"
        assert result.average == 60.0
        assert result.std == 0.0
        assert result.n_events == 2

    def test_calculate_statistics_with_event_type(self) -> None:
        repo_events = {
            "https://github.com/user/repo": [
                {"type": "PushEvent", "created_at": "2023-05-01T12:00:00Z"},
                {"type": "PushEvent", "created_at": "2023-05-01T13:00:00Z"},
                {"type": "PullRequestEvent", "created_at": "2023-05-01T12:01:00Z"},
                {"type": "PullRequestEvent", "created_at": "2023-05-01T13:01:00Z"},
            ]
        }
        result = calculate_statistics(repo_events, event_type="PushEvent")
        assert result is not None
        assert result.repository == "https://github.com/user/repo"
        assert result.average == 3600.0
        assert result.std == 0.0
        assert result.n_events == 2
        assert result.min == "2023-05-01T12:00:00"
        assert result.max == "2023-05-01T13:00:00"
        assert result.timestamps == ["2023-05-01T12:00:00", "2023-05-01T13:00:00"]

    def test_calculate_statistics_no_events(self) -> None:
        data: list[dict[str, Any]] = []
        repo_events = {"https://github.com/user/repo": data}
        result = calculate_statistics(repo_events)
        assert result is None
