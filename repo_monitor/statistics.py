from datetime import datetime
from typing import Optional, Any

import numpy as np

from repo_monitor.models.stats import Statistics


def calculate_duration(timestamp_iso: list[str]) -> list[float]:
    duration = []
    for i in range(len(timestamp_iso) - 1):
        diff = datetime.fromisoformat(timestamp_iso[i + 1]) - datetime.fromisoformat(
            timestamp_iso[i]
        )
        duration.append(float(diff.total_seconds()))
    return duration


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
            timestamps_iso = sorted([timestamp.isoformat() for timestamp in timestamps])
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
