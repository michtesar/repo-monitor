from pydantic import BaseModel
from pydantic_settings import BaseSettings


class Config(BaseModel):
    successful: bool
    results: BaseSettings
