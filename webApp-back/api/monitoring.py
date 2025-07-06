from fastapi import APIRouter
import asyncpg
import os

router = APIRouter()
DATABASE_URL = os.getenv("DATABASE_URL")

@router.get("/monitoring/")
async def get_floors():
    try:
        print("DATABASE_URL:", DATABASE_URL)
        conn = await asyncpg.connect(DATABASE_URL)
        rows = await conn.fetch('SELECT floor_name FROM floor ORDER BY floor_name;')
        print("rows from db:", rows)
        await conn.close()
        return [row["floor_name"] for row in rows]
    except Exception as e:
        print(f"Database connection error: {e}")
        return []