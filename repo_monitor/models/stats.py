from pydantic import BaseModel


class Statistics(BaseModel):
    repository: str
    average: float
    std: float
    min: str
    max: str
    n_events: int
    timestamps: list[str]
    duration: list[float]


class StatisticsSuccess(BaseModel):
    successful: bool = True
    results: Statistics


class StatisticsFailed(BaseModel):
    successful: bool = False
    detail: str
    message: str
