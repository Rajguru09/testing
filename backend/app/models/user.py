from pydantic import BaseModel, EmailStr, Field, model_validator
from enum import Enum
import re

class RoleEnum(str, Enum):
    basic = "basic"
    admin = "admin"  # You can add more roles as needed

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    confirm_password: str

    @model_validator(mode='after')
    def validate_passwords(cls, values):
        password = values.get("password")
        confirm_password = values.get("confirm_password")

        if password != confirm_password:
            raise ValueError("Passwords do not match")

        # Additional password strength check
        if not password_strength(password):
            raise ValueError("Password must contain at least one uppercase letter, one number, and one special character.")
        return values

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    uid: str
    email: EmailStr
    role: RoleEnum = RoleEnum.basic  # Default to basic role

    class Config:
        # Ensure that model output is in snake_case format
        alias_generator = lambda string: string.lower()

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # Default to 1 hour expiration time

    class Config:
        str_strip_whitespace = True

# Password strength check
def password_strength(password: str) -> bool:
    return bool(re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password))
