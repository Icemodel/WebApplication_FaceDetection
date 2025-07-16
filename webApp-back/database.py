# เพิิ่ม sqlalchemy เข้าไป
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv
import os

load_dotenv()

from base import Base 

# ตั้งค่าและเชื่อมต่อกับฐานข้อมูล SQLite
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

# Sync engine/session (สำหรับไฟล์ที่ไม่ใช้ async)
sync_engine = create_engine(SYNC_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

# Async engine/session (สำหรับไฟล์ที่ใช้ async/await)
async_engine = create_async_engine(ASYNC_DATABASE_URL)
AsyncSessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

from models import PersonDB, FloorDB, CameraDB, RoleDB, FacultyDB, DepartmentDB, ContactDB, FloorCameraDB, FloorPersonDB, FaceDB

Base.metadata.create_all(bind=sync_engine)

# Dependency สำหรับสร้าง Session กับฐานข้อมูลในแต่ละคำร้องขอ
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db



