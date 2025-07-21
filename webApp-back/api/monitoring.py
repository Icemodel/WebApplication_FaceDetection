from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_async_db
from models import FloorDB, CameraDB, FloorCameraDB

router = APIRouter()

@router.get("/api/floors/")
async def get_floors(db: AsyncSession = Depends(get_async_db)):
    try:
        result = await db.execute(select(FloorDB).order_by(FloorDB.floor_name))
        floors = result.scalars().all()
        return [floor.floor_name for floor in floors]
    except Exception as e:
        print(f"Database error: {e}")
        return []

@router.get("/api/cameras/")
async def get_cameras_by_floor(floor_name: str = Query(...), db: AsyncSession = Depends(get_async_db)):
    try:
        result = await db.execute(select(FloorDB).where(FloorDB.floor_name == floor_name))
        floor = result.scalar_one_or_none()
        if not floor:
            return []
        result = await db.execute(
            select(CameraDB)
            .join(FloorCameraDB, CameraDB.id == FloorCameraDB.camera_id)
            .where(FloorCameraDB.floor_id == floor.id)
            .order_by(CameraDB.camera_name)
        )
        cameras = result.scalars().all()
        return [{"id": cam.id, "camera_name": cam.camera_name} for cam in cameras]
    except Exception as e:
        print(f"Database error: {e}")
        return []