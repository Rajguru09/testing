import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
import logging

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize DynamoDB resource and client
try:
    dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION)
    dynamodb_client = boto3.client("dynamodb", region_name=settings.AWS_REGION)

    # Reference to the users table
    table = dynamodb.Table(settings.DYNAMODB_TABLE)

    # Check if table exists
    response = dynamodb_client.describe_table(TableName=settings.DYNAMODB_TABLE)
    logger.info(f"DynamoDB table '{settings.DYNAMODB_TABLE}' is accessible.")
except ClientError as e:
    error_code = e.response["Error"]["Code"]
    if error_code == "ResourceNotFoundException":
        logger.error(f"Table '{settings.DYNAMODB_TABLE}' does not exist!")
    else:
        logger.error(f"DynamoDB ClientError: {e.response['Error']['Message']}")
except Exception as e:
    logger.error(f"Unexpected error accessing DynamoDB: {str(e)}")
