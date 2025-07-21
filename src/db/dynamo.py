import boto3
from botocore.exceptions import (BotoCoreError, ClientError,
                                 EndpointConnectionError, NoCredentialsError)

from config import settings
from utils.logger_utils import get_logger

logger = get_logger(__file__)


class DynamoConnector:
    """Singleton class to connect to DynamoDB database."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = boto3.resource(
                    "dynamodb", region_name=settings.aws_region
                )
                logger.info("✅ DynamoDB connection is OK!")
            except EndpointConnectionError as e:
                logger.error(f"❌ Connection error: {e}")
            except NoCredentialsError as e:
                logger.error(f"❌ Credentials not found: {e}")
            except ClientError as e:
                logger.error(f"❌   AWS Client error: {e.response['Error']['Message']}")
            except BotoCoreError as e:
                logger.error(f"❌ General Boto3 error: {e}")
            except Exception as e:
                logger.error(f"❌ Unexpected error: {e}")
        return cls._instance


dynamo_connector = DynamoConnector()
