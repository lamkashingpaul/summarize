from dataclasses import dataclass
from typing import Optional

from src.settings.schemas.internals import ConfiguredGmailConfig


@dataclass
class SendEmailConfig:
    hostname: str
    port: int
    start_tls: bool

    gmail_config: Optional[ConfiguredGmailConfig]


@dataclass
class TokenCache:
    access_token: Optional[str] = None
    expires_at: int = 0
