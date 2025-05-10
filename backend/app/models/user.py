from pydantic import BaseModel, EmailStr, Field, model_validator
from enum import Enum
import re

# Enum for roles
class RoleEnum(str, Enum):
    basic = "basic"
    admin = "admin"

# Password strength check function (regex)
def password_strength(password: str) -> bool:
    return bool(re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password))

# Mobile number validation
def validate_mobile_number(mobile_number: str) -> bool:
    return bool(re.match(r'^\+?[1-9]\d{9,14}$', mobile_number))

# User creation model
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str
    mobile_number: str

    @model_validator(mode="after")
    def validate_all(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        mobile_number = values.get('mobile_number')

        # Passwords must match
        if password != confirm_password:
            raise ValueError("Passwords do not match")

        # Password strength check
        if not password_strength(password):
            raise ValueError("Password must contain at least one uppercase letter, one number, and one special character.")

        # Mobile number validation
        if not validate_mobile_number(mobile_number):
            raise ValueError("Invalid mobile number format. Include country code (e.g., +91...).")

        return values

# User login model
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# User output model (for API response)
class UserOut(BaseModel):
    uid: str
    email: EmailStr
    role: RoleEnum = RoleEnum.basic

    class Config:
        alias_generator = lambda string: string.lower()

# Token output model (for authentication responses)
class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600

    class Config:
        str_strip_whitespace = True
