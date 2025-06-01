import os
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

env = os.getenv("ENV", "development")
env_file = ".env.development.local"
if env == "production":
    env_file = ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding="utf-8")

    env: Literal["development", "production"] = Field(..., description="Environment")

    cohere_api_key: str = Field(description="Cohere API key")

    deepseek_api_key: str = Field(description="DeepSeek API key")

    database_url: PostgresDsn = Field(description="PostgreSQL database URL")

    redis_url: RedisDsn = Field(description="Redis database URL")

    langsmith_tracing: Literal["true"] = Field(description="Enable Langsmith tracing")
    langsmith_endpoint: str = Field(description="Langsmith endpoint")
    langsmith_api_key: str = Field(description="Langsmith API key")
    langsmith_project: str = Field(description="Langsmith project name")

    allow_origins: list[str] = Field(description="Allowed origins for CORS")


settings = Settings.model_validate({})

os.environ["ENV"] = settings.env
os.environ["COHERE_API_KEY"] = settings.cohere_api_key
os.environ["DEEPSEEK_API_KEY"] = settings.deepseek_api_key
os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith_endpoint
os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
os.environ["LANGSMITH_TRACING"] = settings.langsmith_tracing
