from fastapi import APIRouter, Query
import asyncpg
import os

router = APIRouter()
DATABASE_URL = os.getenv("DATABASE_URL")

@router.get("/floors/")
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
    
@router.get("/cameras/")
async def get_cameras_by_floor(floor_name: str = Query(...)):
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        floor_row = await conn.fetchrow('SELECT id FROM floor WHERE floor_name = $1', floor_name)
        if not floor_row:
            await conn.close()
            return []
        floor_id = floor_row['id']
        rows = await conn.fetch('''
            SELECT camera.id, camera.camera_name FROM camera
            JOIN floor_camera ON camera.id = floor_camera.camera_id
            WHERE floor_camera.floor_id = $1
            ORDER BY camera.camera_name                    
        ''', floor_id)
        await conn.close()
        return [{"id": row["id"], "camera_name": row["camera_name"]} for row in rows]
    except Exception as e:
        print(f"Database connection error: {e}")
        return []