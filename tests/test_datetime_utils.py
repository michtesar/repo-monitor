from unittest import TestCase
from datetime import datetime
from repo_monitor.controller import to_datetime
import pytest


class TestToDatetimeHelper(TestCase):
    def test_parse_datetime_valid(self) -> None:
        date_str = "2023-05-01T12:00:00Z"
        expected_datetime = datetime(2023, 5, 1, 12, 0, 0)
        assert to_datetime(date_str) == expected_datetime

    def test_parse_datetime_invalid(self) -> None:
        date_str = "2023-05-01 12:00:00"
        with pytest.raises(ValueError):  # noqa: PT011
            to_datetime(date_str)
