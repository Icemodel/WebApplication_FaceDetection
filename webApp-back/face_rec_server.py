import asyncio
import websockets
from services.face_recognition import process_frame

# เก็บ client ที่เชื่อมต่อ (เช่น capCam, frontend)
connected_clients = set()

async def handler(websocket):
    # เพิ่ม client ใหม่
    connected_clients.add(websocket)
    try:
        async for frame_bytes in websocket:
            # ประมวลผล frame
            processed_bytes = await process_frame(frame_bytes)
            # ส่ง processed frame ไปยังทุก client ที่เชื่อมต่อ (รวม frontend)
            disconnected = set()
            for client in connected_clients:
                try:
                    await client.send(processed_bytes)
                except Exception:
                    disconnected.add(client)
            # ลบ client ที่หลุดออก
            connected_clients.difference_update(disconnected)
    except Exception as e:
        print("Error:", e)
    finally:
        connected_clients.discard(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 3002, max_size=2**24):
        print("Face recognition WebSocket server started on ws://0.0.0.0:3002")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())