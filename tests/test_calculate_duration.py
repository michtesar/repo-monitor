from unittest import TestCase

import pytest

from repo_monitor.lib.statistics import calculate_duration


class TestCalculateDuration(TestCase):
    def test_calculate_duration(self) -> None:
        timestamp_iso = [
            "2023-05-01T12:00:00Z",
            "2023-05-01T12:01:00Z",
            "2023-05-01T12:02:00Z",
        ]
        expected_duration = [60.0, 60.0]
        assert calculate_duration(timestamp_iso) == expected_duration

    def test_calculate_duration_empty_list(self) -> None:
        timestamp_iso: list[str] = []
        assert calculate_duration(timestamp_iso) == []

    def test_calculate_duration_single_timestamp(self) -> None:
        timestamp_iso = ["2023-05-01T12:00:00Z"]
        assert calculate_duration(timestamp_iso) == []

    def test_calculate_duration_invalid_timestamp_format(self) -> None:
        timestamp_iso = ["2023-05-01-12-00-00", "2023-05-01-12-01-00"]
        with pytest.raises(ValueError):  # noqa: PT011
            calculate_duration(timestamp_iso)
