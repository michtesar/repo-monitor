from pydantic import BaseModel


class StatisticsSuccess(BaseModel):
    successful: bool = True
    results: list[dict[str, list]]


class StatisticsFailed(BaseModel):
    successful: bool = False
    detail: str
    message: str
