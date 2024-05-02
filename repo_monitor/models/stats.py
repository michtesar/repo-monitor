from datetime import datetime

from pydantic import BaseModel


class Statistics(BaseModel):
    repository: str
    average: float
    std: float
    min: float
    max: float
    first: datetime
    last: datetime
    n_events: int
    timestamps: list[int]
    inter_timestamps_intervals: list[int]


class StatisticsSuccess(BaseModel):
    successful: bool = True
    results: Statistics


class StatisticsFailed(BaseModel):
    successful: bool = False
    detail: str
    message: str
