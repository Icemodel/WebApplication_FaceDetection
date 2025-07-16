from fastapi import Request
from fastapi.responses import JSONResponse
import jwt
from jwt import PyJWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

EXCLUDE_PATHS = ["/sign-in", "/sign-up", "/docs", "/openapi.json", "/api/signin",]

async def login_required_middleware(request: Request, call_next):
    if request.url.path in EXCLUDE_PATHS:
        return await call_next(request)
    token = request.cookies.get("jwt_token") or request.headers.get("Authorization")
    print("Token from request.cookies.get('jwt_token'):", request.cookies.get("jwt_token"))  # เพิ่ม log ตรงนี้
    print("Token from request.headers.get('Authorization'):", request.headers.get("Authorization"))  # เพิ่ม log ตรงนี้
    print("Token used for validation:", token)  # log token ที่จะใช้ validate
    if not token or not validate_token(token):
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
    return await call_next(request)

def validate_token(token: str) -> bool:
    try:
        print("Token received for validation:", token)
        if token.startswith("Bearer "):
            token = token.split(" ", 1)[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True
    except PyJWTError as e:
        print("JWT error:", e)
        return False
