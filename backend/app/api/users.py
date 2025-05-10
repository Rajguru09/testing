from fastapi import APIRouter, HTTPException
from app.core.db import table
from boto3.dynamodb.conditions import Key
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def sanitize_user(user: dict) -> dict:
    """Remove sensitive fields from the user data."""
    user.pop("password", None)
    return user

@router.get("/")
async def get_users():
    try:
        response = table.scan()
        users = response.get("Items", [])

        if not users:
            raise HTTPException(status_code=404, detail="No users found")

        # Remove sensitive fields from each user
        sanitized_users = [sanitize_user(user) for user in users]
        return {"data": sanitized_users}

    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail="Error fetching users: Internal server error.")

@router.get("/{uid}")
async def get_user(uid: str):
    try:
        response = table.get_item(Key={"uid": uid})
        user = response.get("Item")

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {"data": sanitize_user(user)}

    except Exception as e:
        logger.error(f"Error fetching user with UID {uid}: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user: Internal server error.")
