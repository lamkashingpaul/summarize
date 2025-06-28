from dataclasses import dataclass


@dataclass
class ConfiguredGmailConfig:
    oauth2_token_url: str
    user: str
    client_id: str
    client_secret: str
    refresh_token: str
