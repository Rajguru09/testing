from fastapi import APIRouter, HTTPException
from app.core.db import table
from boto3.dynamodb.conditions import Key

router = APIRouter()

@router.get("/")
async def get_users():
    try:
        # Use scan for simplicity (but consider using query for large datasets or paginated data)
        response = table.scan()
        users = response.get("Items", [])
        
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        
        return {"data": users}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching users: Internal server error.")

@router.get("/{uid}")
async def get_user(uid: str):
    try:
        # Fetch a specific user by UID (consider query if 'uid' is indexed for better performance)
        response = table.get_item(Key={"uid": uid})
        user = response.get("Item")
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"data": user}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching user: Internal server error.")
