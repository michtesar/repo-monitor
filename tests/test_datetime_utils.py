from unittest import TestCase
from datetime import datetime

import pytest

from repo_monitor.lib.statistics import _to_iso, _parse_datetime


class TestDateTimeFunctions(TestCase):
    def test_to_iso_valid(self) -> None:
        date_str = "2023-05-01T12:00:00"
        expected_datetime = datetime(2023, 5, 1, 12, 0, 0)
        assert _to_iso(date_str) == expected_datetime

    def test_to_iso_invalid(self) -> None:
        date_str = "2023-05-01-12-00-00-ABCD"
        with pytest.raises(ValueError):  # noqa: PT011
            _to_iso(date_str)

    def test_parse_datetime_valid(self) -> None:
        date_str = "2023-05-01T12:00:00Z"
        expected_datetime = datetime(2023, 5, 1, 12, 0, 0)
        assert _parse_datetime(date_str) == expected_datetime

    def test_parse_datetime_invalid(self) -> None:
        date_str = "2023-05-01 12:00:00"
        with pytest.raises(ValueError):  # noqa: PT011
            _parse_datetime(date_str)
