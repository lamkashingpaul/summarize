import logging
import logging.config
import time

from src.settings.service import settings


class UTCFormatter(logging.Formatter):
    converter = time.gmtime


def setup_logging():
    """Set up logging configuration."""
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "()": UTCFormatter,
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "simple",
            },
        },
        "loggers": {
            "application": {
                "handlers": ["console"],
                "level": logging.INFO,
                "propagate": False,
            },
        },
    }
    logging.config.dictConfig(logging_config)


def get_default_logger():
    """Get the default logger."""
    if settings.env == "development":
        return logging.getLogger("uvicorn")
    return logging.getLogger("application")


setup_logging()
