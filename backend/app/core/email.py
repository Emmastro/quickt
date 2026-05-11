"""
Email sending service using AWS SES via boto3.
When email_enabled=False (dev), logs to stdout instead of sending.
"""

import logging
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

from app.config import get_settings

logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates" / "emails"


def _get_ses_client():
    settings = get_settings()
    return boto3.client(
        "ses",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id or None,
        aws_secret_access_key=settings.aws_secret_access_key or None,
    )


def load_template(name: str, **kwargs: str) -> str:
    """Load an HTML email template and substitute placeholders."""
    path = TEMPLATES_DIR / f"{name}.html"
    html = path.read_text(encoding="utf-8")
    for key, value in kwargs.items():
        html = html.replace(f"{{{{{key}}}}}", value)
    return html


async def send_email(to: str, subject: str, html_body: str) -> None:
    """Send an HTML email via AWS SES. In dev mode, logs instead of sending."""
    settings = get_settings()

    if not settings.email_enabled:
        logger.info(
            "EMAIL (dev mode, not sent)\n  To: %s\n  Subject: %s\n  Body:\n%s",
            to, subject, html_body,
        )
        print(f"\n{'='*60}")
        print(f"EMAIL TO: {to}")
        print(f"SUBJECT: {subject}")
        print(f"{'='*60}")
        print(html_body)
        print(f"{'='*60}\n")
        return

    client = _get_ses_client()
    source = f"{settings.aws_ses_sender_name} <{settings.aws_ses_sender_email}>"

    send_kwargs: dict = {
        "Source": source,
        "Destination": {"ToAddresses": [to]},
        "Message": {
            "Subject": {"Data": subject, "Charset": "UTF-8"},
            "Body": {"Html": {"Data": html_body, "Charset": "UTF-8"}},
        },
    }
    if settings.aws_ses_configuration_set:
        send_kwargs["ConfigurationSetName"] = settings.aws_ses_configuration_set

    try:
        response = client.send_email(**send_kwargs)
        logger.info("SES email sent to %s — MessageId: %s", to, response["MessageId"])
    except ClientError:
        logger.exception("Failed to send email via SES to %s", to)
        raise
