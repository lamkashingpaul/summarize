from src.mails.service import send_email
from src.settings.service import settings


async def send_verification_email_task(email: str, token: str) -> None:
    subject = "Please verify your email address"
    plain = (
        f"Click the link to verify your email:\n"
        f"{settings.web_base_url}/auth/verify-email?email={email}&token={token}"
    )

    await send_email(bcc_emails=[email], subject=subject, plain=plain, html=plain)
