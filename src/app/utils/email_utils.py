from functools import partial

from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig,
    MessageType
)

from app.core.config import settings


def send_email_notification(
    subject: str,
    body: str
) -> partial | None:

    if settings.EMAIL_RECIPIENTS:
        conf = ConnectionConfig(
            MAIL_USERNAME = settings.SMTP_USER,
            MAIL_PASSWORD = settings.SMTP_PASSWORD,
            MAIL_FROM = settings.SMTP_USER,
            MAIL_PORT = settings.SMTP_PORT,
            MAIL_SERVER = settings.SMTP_HOST,
            MAIL_SSL_TLS = settings.SMTP_SSL_TLS,
            MAIL_STARTTLS = True
        )

        message = MessageSchema(
            subject = subject,
            recipients = settings.EMAIL_RECIPIENTS,
            body = body,
            subtype=MessageType.plain
        )

        fast_mail = FastMail(conf)
        return partial(fast_mail.send_message, message)