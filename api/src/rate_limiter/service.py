from slowapi import Limiter
from slowapi.util import get_remote_address

from src.settings.service import settings

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=settings.redis_url.encoded_string(),
    default_limits=["100/minute"],
)
