import asyncio
import base64
import time

import aiohttp

from src.mails.schemas.internals import TokenCache
from src.settings.schemas.internals import ConfiguredGmailConfig

_token_cache = TokenCache(
    access_token=None,
    expires_at=0,
)

_token_lock = asyncio.Lock()
TOKEN_BUFFER_SECONDS = 60


async def request_gmail_oauth2_access_token(
    token_url: str, client_id: str, client_secret: str, refresh_token: str
) -> tuple[str, int]:
    async with aiohttp.ClientSession() as session:
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        async with session.post(token_url, data=data) as response:
            if response.status != 200:
                raise Exception("Failed to fetch access token")

            token_data = await response.json()
            return token_data["access_token"], token_data.get("expires_in", 3600)


def generate_xoauth2_auth_string(user: str, access_token: str) -> bytes:
    auth_string = f"user={user}\x01auth=Bearer {access_token}\x01\x01"
    return base64.b64encode(auth_string.encode("utf-8"))


async def generate_gmail_xoauth2_payload(gmail_config: ConfiguredGmailConfig) -> bytes:
    global _token_cache

    token_url = gmail_config.oauth2_token_url
    user = gmail_config.user
    client_id = gmail_config.client_id
    client_secret = gmail_config.client_secret
    refresh_token = gmail_config.refresh_token

    current_time = time.time()
    if (
        _token_cache.access_token
        and _token_cache.expires_at > current_time + TOKEN_BUFFER_SECONDS
    ):
        return generate_xoauth2_auth_string(user, _token_cache.access_token)

    async with _token_lock:
        if (
            _token_cache.access_token
            and _token_cache.expires_at > current_time + TOKEN_BUFFER_SECONDS
        ):
            return generate_xoauth2_auth_string(user, _token_cache.access_token)

        try:
            access_token, expires_in = await request_gmail_oauth2_access_token(
                token_url=token_url,
                client_id=client_id,
                client_secret=client_secret,
                refresh_token=refresh_token,
            )

            _token_cache.access_token = access_token
            _token_cache.expires_at = int(current_time) + expires_in

            auth_string = generate_xoauth2_auth_string(user, access_token)
            return auth_string

        except Exception as e:
            _token_cache.access_token = None
            _token_cache.expires_at = 0
            raise e
