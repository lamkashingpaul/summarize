import functools
from email.message import EmailMessage

import aiosmtplib

from src.mails.schemas.internals import SendEmailConfig
from src.mails.utils import generate_gmail_xoauth2_payload
from src.settings.schemas.internals import ConfiguredGmailConfig
from src.settings.service import is_gmail_configured, settings


@functools.cache
async def get_send_email_config() -> SendEmailConfig:
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
        gmail_config=None,
    )

    if is_gmail_configured(smtp_settings.gmail):
        gmail_config = ConfiguredGmailConfig(
            oauth2_token_url=smtp_settings.gmail.oauth2_token_url,
            user=smtp_settings.gmail.user,
            client_id=smtp_settings.gmail.client_id,
            client_secret=smtp_settings.gmail.client_secret,
            refresh_token=smtp_settings.gmail.refresh_token,
        )
        send_email_config.gmail_config = gmail_config

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

    send_email_config = await get_send_email_config()
    gmail_config = send_email_config.gmail_config

    smtp_client = aiosmtplib.SMTP(
        hostname=send_email_config.hostname,
        port=send_email_config.port,
        start_tls=send_email_config.start_tls,
        use_tls=send_email_config.use_tls,
    )

    async with smtp_client:
        if gmail_config:
            auth_string = await generate_gmail_xoauth2_payload(gmail_config)
            await smtp_client.execute_command(b"AUTH XOAUTH2", b"XOAUTH2", auth_string)

        await smtp_client.send_message(message)
