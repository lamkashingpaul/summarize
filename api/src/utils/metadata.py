from typing import ClassVar, Final


class LoggingMetadata:
    KEY: ClassVar[str] = "__fastapi_request_logging_metadata__"

    def __init__(self, enabled: bool):
        self.enabled = enabled


LOG_METADATA_KEY: Final[str] = LoggingMetadata.KEY
