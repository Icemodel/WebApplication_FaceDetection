# เพิิ่ม sqlalchemy เข้าไป
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

from base import Base 

# ตั้งค่าและเชื่อมต่อกับฐานข้อมูล SQLite
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# instance class เริ่มต้นสำหรับ engine, SessionLocal และ Base
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from models import PersonDB, FloorDB, CameraDB, RoleDB, FacultyDB, DepartmentDB, ContactDB, FloorCameraDB, FloorPersonDB, FaceDB

Base.metadata.create_all(bind=engine)

# Dependency สำหรับสร้าง Session กับฐานข้อมูลในแต่ละคำร้องขอ
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)  # สร้างตารางใหม่


