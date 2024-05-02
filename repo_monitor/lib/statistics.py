from datetime import datetime
from typing import Optional, Any

import numpy as np

from repo_monitor.models.stats import Statistics


def _to_iso(date: str) -> datetime:
    """Helper function to convert datetime to ISO string"""
    return datetime.fromisoformat(date)


def _parse_datetime(date: str) -> datetime:
    """Helper function to parse datetime string to datetime object"""
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")


def calculate_duration(timestamp_iso: list[str]) -> list[float]:
    """
    Calculate interval duration in between each consecutive
    timestamps in the list of IS0 formatted date times.
    :param timestamp_iso: List of ISO date times
    :return: List of durations in seconds
    """
    duration = []
    for i in range(len(timestamp_iso) - 1):
        diff = _to_iso(timestamp_iso[i + 1]) - _to_iso(timestamp_iso[i])
        duration.append(float(diff.total_seconds()))
    return duration


def calculate_statistics(
    repo_events: dict[str, list[dict[str, Any]]],
    event_type: Optional[str] = None,
) -> Optional[Statistics]:
    """
    Calculate repository statistics, including average and std
    per times and report number or processed events.
    :param repo_events: All the events from the repository
    :param event_type: Optional filter to process only selected
        event type, such as PushEvent for example.
    :return: Repository statistics object if available, None otherwise
    """
    for url, events in repo_events.items():
        # Filter the events
        filtered_events = events
        if event_type:
            filtered_events = [event for event in events if event["type"] == event_type]

        # Process only filtered events
        if filtered_events:
            timestamps = [_parse_datetime(event["created_at"]) for event in filtered_events]
            # Get and sort all events by timestamp in ISO format
            timestamps_iso = sorted([timestamp.isoformat() for timestamp in timestamps])

            # Calculate duration in between the timestamps
            duration = calculate_duration(timestamps_iso)

            return Statistics(
                repository=url,
                average=np.mean(duration),
                std=np.std(duration),
                min=min(timestamps_iso),
                max=max(timestamps_iso),
                n_events=len(filtered_events),
                timestamps=timestamps_iso,
                duration=duration,
            )
    return None
