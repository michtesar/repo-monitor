from datetime import datetime
from typing import Any, Optional

from requests_cache import CachedSession


def to_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")


def get_github_events(
    url: Optional[str], session: CachedSession
) -> list[dict[str, datetime | Any]]:
    events = []

    while url:
        response = session.get(url)
        response.raise_for_status()

        for event in response.json():
            event_data = {
                "type": event["type"],
                "created_at": to_datetime(event["created_at"]),
            }
            events.append(event_data)

        # Check for a pagination link in response headers
        link_header = response.headers.get("Link")
        if link_header:
            next_link = None
            for link in link_header.split(","):
                parts = link.split(";")
                if len(parts) == 2 and 'rel="next"' in parts[1]:
                    next_link = parts[0].strip()[1:-1]
                    break
            url = next_link
        else:
            url = None

    # Return the events sorted by the timestamp
    return sorted(events, key=lambda event: event["created_at"])


def slice_by_weeks(events: list[dict]) -> list[list[dict]]:
    week_number = events[0]["created_at"].isocalendar()[1]
    chunks: list[list[dict[str, str | datetime]]] = []
    chunk: list[dict[str, str | datetime]] = []
    for event in events:
        current_week = event["created_at"].isocalendar()[1]
        if week_number is not current_week:
            week_number = current_week
            chunks.append(chunk)
            chunk = []
        chunk.append(event)
    return chunks


def create_sliding_window(events: list[dict], n: int = 500) -> list[list[dict]]:
    if len(events) > n:
        chunks = [events[i : i + n] for i in range(0, len(events), n)]
    else:
        chunks = slice_by_weeks(events)
    return chunks


def calculate_statistics(data: list[dict]) -> dict[str, float]:
    time_diffs: dict[Any, list[float]] = {}
    average_time_diffs = {}
    for i in range(1, len(data)):
        event_type = data[i]["type"]

        time_diff = data[i]["created_at"] - data[i - 1]["created_at"]

        if event_type not in time_diffs:
            time_diffs[event_type] = []

        time_diffs[event_type].append(time_diff.total_seconds())

        for event_type, diffs in time_diffs.items():
            average_time_diffs[event_type] = sum(diffs) / len(diffs) if len(diffs) > 0 else 0

    return average_time_diffs


def get_statistics_by_event_type(api_url: str, session: CachedSession) -> dict[str, list]:
    events = get_github_events(api_url, session)
    chunks = create_sliding_window(events)
    results: dict[str, list] = {api_url: []}
    for chunk in chunks:
        stats = calculate_statistics(chunk)
        results[api_url].append(stats)
    return results


def create_api_url(url: str) -> str:
    """Construct API url from GitHub repo url"""
    *_, owner, repo = url.split("/")
    return f"https://api.github.com/repos/{owner}/{repo}/events"
