import os
from typing import Literal, Optional, TypeGuard

from pydantic import Field, PostgresDsn, RedisDsn, computed_field
from pydantic_settings import SettingsConfigDict

from src.settings.schemas.internals import ConfiguredGmailConfig
from src.settings.utils import CustomBaseSettings

Environment = Literal["development", "production"]

env = os.getenv("ENV", "development")
env_file = ".env.development.local"
if env == "production":
    env_file = ".env"


class GmailConfig(CustomBaseSettings):
    oauth2_token_url: Optional[str] = Field(description="Gmail OAuth2 token URL")
    user: Optional[str] = Field(description="Gmail user email address")
    client_id: Optional[str] = Field(description="Gmail OAuth2 client ID")
    client_secret: Optional[str] = Field(description="Gmail OAuth2 client secret")
    refresh_token: Optional[str] = Field(description="Gmail OAuth2 refresh token")

    @computed_field(description="Check if Gmail is configured")
    @property
    def is_gmail_configured(self) -> bool:
        return all(
            [
                self.oauth2_token_url,
                self.user,
                self.client_id,
                self.client_secret,
                self.refresh_token,
            ]
        )


class SmtpConfig(CustomBaseSettings):
    host: str = Field(description="SMTP server host")
    port: int = Field(description="SMTP server port")
    gmail: GmailConfig


class AuthConfig(CustomBaseSettings):
    session_expires_in: int = Field(description="Session expiration time in seconds")


class LangsmithConfig(CustomBaseSettings):
    tracing: Literal["true"] = Field(description="Enable Langsmith tracing")
    endpoint: str = Field(description="Langsmith endpoint")
    api_key: str = Field(description="Langsmith API key")
    project: str = Field(description="Langsmith project name")


class Settings(CustomBaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    env: Environment = Field(description="Environment")

    cohere_api_key: str = Field(description="Cohere API key")

    deepseek_api_key: str = Field(description="DeepSeek API key")

    database_url: PostgresDsn = Field(description="PostgreSQL database URL")

    redis_url: RedisDsn = Field(description="Redis database URL")

    allow_origins: list[str] = Field(description="Allowed origins for CORS")

    web_base_url: str = Field(description="Base URL for the web application")

    langsmith: LangsmithConfig
    auth: AuthConfig
    smtp: SmtpConfig


def is_gmail_configured(config: GmailConfig) -> TypeGuard[ConfiguredGmailConfig]:
    return config.is_gmail_configured


settings = Settings.model_validate({})

os.environ["ENV"] = settings.env
os.environ["COHERE_API_KEY"] = settings.cohere_api_key
os.environ["DEEPSEEK_API_KEY"] = settings.deepseek_api_key
os.environ["LANGSMITH_API_KEY"] = settings.langsmith.api_key
os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith.endpoint
os.environ["LANGSMITH_PROJECT"] = settings.langsmith.project
os.environ["LANGSMITH_TRACING"] = settings.langsmith.tracing
