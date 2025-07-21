from fastapi import APIRouter, Query, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_async_db
from models import UserDB
import os
import jwt

router = APIRouter()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

@router.get("/api/user/profileIcon")
async def get_user_profile_icon(request:Request, db: AsyncSession = Depends(get_async_db)):
    token = request.cookies.get("jwt_token")
    if not token:
        return {"message": "No token found"}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get("user_id")
        if not user_id:
            return {"message": "No id found in token"}
        result = await db.execute(select(UserDB).where(UserDB.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            return {"message": "User not found in database"}
        elif not user.picture:
            return {"message": "Profile icon not found in database"}
        return {"profile_icon": user.picture}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Error when fetching user profile picture"}
    


    

