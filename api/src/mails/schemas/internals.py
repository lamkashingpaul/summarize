from dataclasses import dataclass


@dataclass
class SendEmailConfig:
    hostname: str
    port: int
    start_tls: bool
    use_tls: bool
