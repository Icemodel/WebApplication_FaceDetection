# เพิิ่ม sqlalchemy เข้าไป
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# ตั้งค่าและเชื่อมต่อกับฐานข้อมูล SQLite
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# instance class เริ่มต้นสำหรับ engine, SessionLocal และ Base
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency สำหรับสร้าง Session กับฐานข้อมูลในแต่ละคำร้องขอ
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)  # สร้างตารางใหม่


