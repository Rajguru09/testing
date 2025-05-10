from pydantic import BaseModel, EmailStr, Field, model_validator
from enum import Enum
import re

# Enum for roles
class RoleEnum(str, Enum):
    basic = "basic"
    admin = "admin"  # You can add more roles as needed

# User creation model
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str
    mobile_number: str

    @model_validator(mode='after')
    def validate_passwords(cls, values):
        password = values.get("password")
        confirm_password = values.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            raise ValueError("Passwords do not match")

        # Additional password strength check (must have uppercase, number, special char)
        if not password_strength(password):
            raise ValueError("Password must contain at least one uppercase letter, one number, and one special character.")
        
        # Validate mobile number
        mobile_number = values.get("mobile_number")
        if not validate_mobile_number(mobile_number):
            raise ValueError("Invalid mobile number format. Ensure it includes country code.")
        
        return values

# User login model
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# User output model (for API response)
class UserOut(BaseModel):
    uid: str
    email: EmailStr
    role: RoleEnum = RoleEnum.basic  # Default to basic role

    class Config:
        # Ensure that model output is in snake_case format
        alias_generator = lambda string: string.lower()

# Token output model (for authentication responses)
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # Default to 1 hour expiration time

    class Config:
        str_strip_whitespace = True

# Password strength check function (regex)
def password_strength(password: str) -> bool:
    # Password must contain at least one uppercase letter, one number, and one special character
    return bool(re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password))

# Mobile number validation (basic check for country code and number)
def validate_mobile_number(mobile_number: str) -> bool:
    # Simple regex for validating mobile number with country code (e.g., +1-555-5555555)
    return bool(re.match(r'^\+?1?\d{9,15}$', mobile_number))  # Modify for specific country code validation
