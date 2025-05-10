import boto3
from botocore.exceptions import ClientError
from app.core.config import settings
import logging

# Set up logging to track the operation results
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize DynamoDB resource and client using the region from settings
dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION)  # Use region from config
dynamodb_client = boto3.client("dynamodb", region_name=settings.AWS_REGION)  # Use region from config

# Table resource using the table name from settings
table = dynamodb.Table(settings.DYNAMODB_TABLE)

# Test to ensure we can access the table
try:
    # Use the client to describe the table
    response = dynamodb_client.describe_table(TableName=settings.DYNAMODB_TABLE)
    logger.info(f"Table '{settings.DYNAMODB_TABLE}' exists!")
except ClientError as e:
    # More specific error handling for DynamoDB-related errors
    error_code = e.response["Error"]["Code"]
    if error_code == "ResourceNotFoundException":
        logger.error(f"Table '{settings.DYNAMODB_TABLE}' does not exist!")
    else:
        logger.error(f"Error accessing table: {e.response['Error']['Message']}")
except Exception as e:
    logger.error(f"An unexpected error occurred: {str(e)}")
