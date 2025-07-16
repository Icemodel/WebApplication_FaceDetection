from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from datetime import datetime, timezone
import jwt
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_async_db
from models import UserDB

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

@router.post("/api/signin")
async def sign_in(request: Request, db: AsyncSession = Depends(get_async_db)):
    data = await request.json()
    print(f"Request data log: {data}") #Dev
    username = data.get("username")
    password = data.get("password")

    result = await db.execute(
        select(UserDB).where(UserDB.username == username)
    )
    user = result.scalar_one_or_none()
    print(f"User row log: {user}") #Dev

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not pwd_context.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email is not verified")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account has been suspended")

    # อัปเดต last_login_at
    user.last_login_at = datetime.now(timezone.utc)
    await db.commit()

    # สร้าง JWT token
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": int(datetime.now(timezone.utc).timestamp()) + 60 * 60 * 24  # 1 วัน
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    response = JSONResponse(content={"message": "Login successful"})
    # เซ็ต cookie JWT
    response.set_cookie(
        key="jwt_token",
        value=token,
        httponly=True,      # ปลอดภัยจาก XSS
        secure=False,       # เปลี่ยนเป็น True ถ้าใช้ HTTPS
        samesite="lax",     # หรือ "strict" ตามต้องการ
        path="/"
    )

    return response