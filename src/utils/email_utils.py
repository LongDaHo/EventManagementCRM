import boto3

from config import settings
from utils.logger_utils import get_logger

logger = get_logger(__name__)

ses_client = boto3.client("ses", region_name=settings.aws_region)


async def send_email_via_ses(to: str, subject: str, body: str):
    logger.info(f"Sending email to {to} with subject {subject} and body {body}")
    ses_client.send_email(
        Source=settings.aws_ses_sender_email,
        Destination={"ToAddresses": [to]},
        Message={"Subject": {"Data": subject}, "Body": {"Text": {"Data": body}}},
        ConfigurationSetName=settings.aws_ses_config_set,
    )
