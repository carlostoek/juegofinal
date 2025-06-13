from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    admin_ids: List[int] = []

    @field_validator("admin_ids", mode="before")
    @classmethod
    def parse_admin_ids(cls, v):
        if not v:
            return []
        if isinstance(v, str):
            return [int(x) for x in v.split(',') if x]
        return v

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
