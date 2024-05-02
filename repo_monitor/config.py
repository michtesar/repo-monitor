from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    cache_expiration_sec: int = 300
    max_repositories: int = 5


settings = Settings()
