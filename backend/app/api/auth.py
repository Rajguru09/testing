from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate, UserLogin, TokenOut
from app.core.security import hash_password, verify_password, create_access_token
from app.core.db import table
import uuid
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def get_user_by_email(email: str):
    response = table.get_item(Key={"email": email})
    return response.get("Item")

# Signup route
@router.post("/signup", response_model=TokenOut)
def signup(user_data: UserCreate):
    existing_user = get_user_by_email(user_data.email)
    if existing_user:
        logger.warning(f"Signup failed: Email {user_data.email} already registered.")
        raise HTTPException(status_code=400, detail="Email already registered")

    # Add validation for mobile number (check for country code and format)
    if not validate_mobile_number(user_data.mobile_number):
        logger.warning(f"Signup failed: Invalid mobile number format for {user_data.mobile_number}.")
        raise HTTPException(status_code=400, detail="Invalid mobile number format. Ensure it includes country code.")
    
    uid = str(uuid.uuid4())
    hashed_pwd = hash_password(user_data.password)

    try:
        # Save user data including mobile number
        table.put_item(Item={
            "uid": uid,
            "email": user_data.email,
            "password": hashed_pwd,
            "role": "basic",
            "mobile_number": user_data.mobile_number  # Store mobile number
        })
        logger.info(f"User {user_data.email} successfully signed up.")
    except Exception as e:
        logger.error(f"Error saving user: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving user: {str(e)}")

    token = create_access_token({
        "sub": user_data.email,
        "uid": uid,
        "role": "basic"
    })
    return {"access_token": token, "token_type": "bearer"}

# Login route
@router.post("/login", response_model=TokenOut)
def login(user_data: UserLogin):
    db_user = get_user_by_email(user_data.email)

    if not db_user:
        logger.warning(f"Login failed: User with email {user_data.email} not found.")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user_data.password, db_user["password"]):
        logger.warning(f"Login failed: Incorrect password for {user_data.email}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "sub": user_data.email,
        "uid": db_user["uid"],
        "role": db_user.get("role", "basic")
    })
    logger.info(f"User {user_data.email} logged in successfully.")
    return {"access_token": token, "token_type": "bearer"}

# Mobile number validation (simple check for country code and number format)
def validate_mobile_number(mobile_number: str) -> bool:
    # Simple regex for validating mobile number with country code (e.g., +1-555-5555555)
    return bool(re.match(r'^\+?1?\d{9,15}$', mobile_number))  # Modify for specific country code validation
