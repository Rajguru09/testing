import uuid
import boto3
from botocore.exceptions import ClientError
from passlib.context import CryptContext
import os

# Initialize DynamoDB connection (with correct region and table)
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')  # Correct region
table = dynamodb.Table('users')  # Correct table name

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(user_data):
    # Generate unique user ID
    user_id = str(uuid.uuid4())
    
    # Hash the password before saving it
    hashed_password = pwd_context.hash(user_data.password)

    try:
        # Insert new user into DynamoDB table with email uniqueness check
        table.put_item(
            Item={
                "uid": user_id,
                "email": user_data.email,
                "password": hashed_password,
                "role": "basic"  # Default role is "basic"
            },
            ConditionExpression="attribute_not_exists(email)"  # Ensure the email is unique
        )
        
    except ClientError as e:
        # Handle specific error for email duplication
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            raise ValueError("User with this email already exists.")
        else:
            raise  # Re-raise any other errors for further handling

    # Return user data (excluding password for security)
    return {
        "uid": user_id,
        "email": user_data.email,
        "role": "basic"  # Default role can be customized
    }
