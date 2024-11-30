from fastapi import HTTPException, Header
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

def auth_middleware(x_auth_token = Header()):
    if not x_auth_token:
        raise HTTPException(401, "Access denied, no token provided")
    
    try:
        token_data = jwt.decode(x_auth_token, os.getenv("PASSWORD_KEY"), algorithms=["HS256"])
        user_id = token_data.get("id")
        
        if not user_id:
            raise HTTPException(401, "Invalid token: user ID not found")
        
        return {"id": user_id, "token": x_auth_token}

    except jwt.InvalidTokenError:
        raise HTTPException(401, "Unauthorized access, invalid token")