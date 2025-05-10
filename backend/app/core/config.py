import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings:
    # Project name used in the application
    PROJECT_NAME: str = "CleanCloud"
    
    # JWT Secret and Algorithm for secure token handling
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")  # Secret key for JWT
    JWT_ALGORITHM: str = "HS256"  # JWT algorithm used for encoding/decoding tokens
    
    # DynamoDB settings
    DYNAMODB_TABLE: str = os.getenv("DYNAMODB_TABLE", "users")  # DynamoDB table name
    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")  # Default AWS region for DynamoDB

    # Validate essential environment variables
    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY is not set in the environment variables")

# Create an instance of Settings to access configuration values
settings = Settings()
