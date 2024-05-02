from pydantic_settings import BaseSettings


class _Settings(BaseSettings):
    cache_expiration_sec: int = 300
    max_repositories: int = 5


settings = _Settings()
