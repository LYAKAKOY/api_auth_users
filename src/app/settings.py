from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresDB(BaseModel):
    user: str
    password: str
    host: str
    port: int
    database: str


class JWT(BaseModel):
    access_token_expire_minutes: int
    secret_key: str
    algorithm: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter=".",
    )

    postgres: PostgresDB
    jwt: JWT


settings = Settings()  # type: ignore
