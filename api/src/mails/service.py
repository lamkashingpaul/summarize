import functools
from dataclasses import asdict
from email.message import EmailMessage

import aiosmtplib

from src.mails.schemas.internals import SendEmailConfig
from src.settings.service import settings


@functools.cache
def get_send_email_config() -> SendEmailConfig:
    smtp_settings = settings.smtp

    hostname = smtp_settings.host
    port = smtp_settings.port
    start_tls = False
    use_tls = False

    send_email_config = SendEmailConfig(
        hostname=hostname,
        port=port,
        start_tls=start_tls,
        use_tls=use_tls,
    )

    return send_email_config


async def send_email(
    bcc_emails: list[str], subject: str, plain: str, html: str
) -> None:
    message = EmailMessage()
    message["From"] = settings.smtp.gmail.user or "foo@bar.com"
    message["Bcc"] = ", ".join(bcc_emails)
    message["Subject"] = subject

    message.set_content(plain)
    message.add_alternative(html, subtype="html")

    send_email_config = get_send_email_config()

    await aiosmtplib.send(message, **asdict(send_email_config))
