from pydantic import BaseModel


class Health(BaseModel):
    status: int
    ready: str
