import os
from typing import Literal
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

env = os.getenv("ENV", "development")
env_file = ".env.development.local"
if env == "production":
    env_file = ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_file, env_file_encoding="utf-8")

    env: Literal["development", "production"] = Field(description="Environment")

    cohere_api_key: str = Field(description="Cohere API key")

    database_url: PostgresDsn = Field(description="PostgreSQL database URL")

    langsmith_tracing: Literal["true"] = Field(description="Enable Langsmith tracing")
    langsmith_endpoint: str = Field(description="Langsmith endpoint")
    langsmith_api_key: str = Field(description="Langsmith API key")
    langsmith_project: str = Field(description="Langsmith project name")

    unstructured_api_key: str = Field(description="Unstructured API key")
    unstructured_api_url: str = Field(description="Unstructured API URL")


settings = Settings.model_validate({})
