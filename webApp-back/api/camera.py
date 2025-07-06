from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
from services.face_recognition import process_frame_logic

router = APIRouter()

# --- Global State for WebSocket Communication ---
clients = set()
latest_frame = None

@router.websocket("/ws/client")
async def client_ws(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    print(f"Frontend client connected (total: {len(clients)})")
    if latest_frame:
        try:
            await websocket.send_bytes(latest_frame)
        except Exception as e:
            print(f"Error sending initial frame to new client: {e}")
    try:
        while True:
            await websocket.receive_text() # รอรับข้อมูล (ถ้ามี) เพื่อให้รู้ว่า client ยังอยู่
    except WebSocketDisconnect:
        print("Frontend client disconnected")
    finally:
        clients.discard(websocket)
        print(f"Client disconnected (total: {len(clients)})")

@router.websocket("/ws/camera")
async def camera_ws(websocket: WebSocket):
    global latest_frame
    await websocket.accept()
    print("Camera connected")
    try:
        while True:
            frame_bytes = await websocket.receive_bytes()
            processed_frame = await process_frame_logic(frame_bytes)
            latest_frame = processed_frame
            
            await websocket.send_bytes(processed_frame) # ส่งกลับให้กล้อง (ถ้าต้องการ)
            
            if clients:
                await asyncio.gather(
                    *(client.send_bytes(processed_frame) for client in clients),
                    return_exceptions=True
                )
    except WebSocketDisconnect:
        print("Camera disconnected")
    except Exception as e:
        print(f"Error in camera websocket: {e}")
    finally:
        print("Camera connection closed")