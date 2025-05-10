from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.core.config import settings
import logging

# Initialize logger
logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Custom exception for security-related errors
class SecurityError(Exception):
    pass

# Generate JWT access token
def create_access_token(data: dict, expires_delta: int = None) -> str:
    """
    Create a JWT access token with expiration.
    
    Args:
        data (dict): User-specific data like email, uid, role.
        expires_delta (int, optional): Expiration in seconds. Defaults to 3600 (1 hour).
    
    Returns:
        str: Encoded JWT access token.
    """
    expires_delta = expires_delta or 3600  # Default to 1 hour
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    to_encode.update({"exp": expire})

    try:
        token = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        logger.info(f"Access token created for user: {data.get('sub')}")
        return token
    except JWTError as e:
        logger.error(f"JWT encoding failed: {e}")
        raise SecurityError("Token creation failed.")
    except Exception as e:
        logger.error(f"Unexpected error in token creation: {e}")
        raise SecurityError("Unexpected error in creating access token.")

# Verify a plain password against its hashed version
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compare plain password with hashed password.
    
    Args:
        plain_password (str): Raw password input.
        hashed_password (str): Password from DB.
    
    Returns:
        bool: True if matched, False otherwise.
    """
    try:
        verified = pwd_context.verify(plain_password, hashed_password)
        logger.info("Password verified successfully." if verified else "Password verification failed.")
        return verified
    except Exception as e:
        logger.error(f"Password verification error: {e}")
        raise SecurityError("Password verification failed.")

# Hash a password before storing
def hash_password(password: str) -> str:
    """
    Hash plain password using bcrypt.
    
    Args:
        password (str): Raw password.
    
    Returns:
        str: Hashed password.
    """
    try:
        hashed = pwd_context.hash(password)
        logger.info("Password hashed successfully.")
        return hashed
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        raise SecurityError("Password hashing failed.")
