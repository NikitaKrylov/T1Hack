from datetime import timezone, timedelta, tzinfo

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    dbuser: str
    dbpassword: str
    dbhost: str
    dbname: str
    dbport: int
    mode: str
    redisport: int
    redishost: str

    @property
    def is_prod(self) -> bool:
        return self.mode == "PROD"

    @property
    def db_url(self) -> str:
        return f'postgresql+asyncpg://{self.dbuser}:{self.dbpassword}@{self.dbhost}:{self.dbport}/{self.dbname}'

    @property
    def redis_url(self) -> str:
        return f'redis://{self.redishost}:{self.redisport}'

    @property
    def time_zone_ino(self) -> tzinfo:
        return timezone(timedelta(hours=3))


config = Config(_env_file='backend.env', _env_file_encoding='utf-8')
