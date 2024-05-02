from datetime import datetime
from typing import Optional, Any, TypeVar

import numpy as np

from repo_monitor.models.stats import Statistics

T = TypeVar("T", int, float)


def calculate_intervals(array: list[T]) -> list[T]:
    intervals = []
    for i in range(1, len(array)):
        interval = array[i] - array[i - 1]
        intervals.append(interval)
    return intervals


def calculate_statistics(
    repo_events: dict[str, list[dict[str, Any]]],
    event_type: Optional[str] = None,
) -> Optional[Statistics]:
    for url, events in repo_events.items():
        filtered_events = events
        if event_type:
            filtered_events = [event for event in events if event["type"] == event_type]

        if filtered_events:
            timestamps = [
                datetime.strptime(event["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                for event in filtered_events
            ]
            timestamps_seconds = sorted([int(timestamp.timestamp()) for timestamp in timestamps])
            timestamps_iso = sorted([timestamp.isoformat() for timestamp in timestamps])

            return Statistics(
                repository=url,
                average=np.mean(timestamps_seconds),
                std=np.std(timestamps_seconds),
                min=np.min(timestamps_seconds),
                max=np.max(timestamps_seconds),
                first=min(timestamps),
                last=max(timestamps),
                n_events=len(filtered_events),
                timestamps=timestamps_iso,
                inter_timestamps_intervals=calculate_intervals(timestamps_seconds),
            )
    return None
