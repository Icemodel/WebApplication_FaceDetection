import uvicorn
import websockets
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

app = FastAPI()
server_url = "ws://127.0.0.1:9000"

clients = set()  # เก็บ WebSocket ของ frontend ทุกตัว
latest_frame = None  # เก็บ processed frame ล่าสุด

@app.websocket("/ws/client")
async def client_ws(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    print(f"Frontend client connected (total: {len(clients)})")
    # ส่ง frame ล่าสุดให้ client ใหม่ทันที (ถ้ามี)
    if latest_frame:
        try:
            await websocket.send_bytes(latest_frame)
            print("Sent latest frame to new client")
        except Exception as e:
            print(f"Error sending latest frame to new client: {e}")
    try:
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print(f"Exception in /ws/client: {e}")
    except WebSocketDisconnect:
        print("Frontend client disconnected")
    finally:
        clients.discard(websocket)
        print(f"Client disconnected (total: {len(clients)})")

@app.websocket("/ws/camera")
async def camera_ws(websocket: WebSocket):
    global latest_frame
    await websocket.accept()
    print("Camera connected")
    try:
        async with websockets.connect(server_url) as server_socket:
            print("Connected to server at 9000")
            while True:
                try:
                    frame_bytes = await websocket.receive_bytes()
                    print("Received frame from camera")
                    await server_socket.send(frame_bytes)
                    print("Sent frame to server")
                    processed_frame = await server_socket.recv()
                    print(f"Received processed frame from server, size: {len(processed_frame)} bytes")
                    latest_frame = processed_frame  # อัปเดต frame ล่าสุด
                    # ส่ง processed frame กลับไป camera.py
                    await websocket.send_bytes(processed_frame)
                    # --- Broadcast section ---
                    dead_clients = set()
                    print(f"Broadcasting to {len(clients)} clients")
                    for client in clients:
                        try:
                            print(f"Try sending processed frame to client, size: {len(processed_frame)} bytes")
                            if processed_frame:
                                await client.send_bytes(processed_frame)
                                print(f"Sent processed frame to client, size: {len(processed_frame)} bytes")
                            else:
                                print("Warning: processed_frame is empty, not sending to client")
                        except Exception as e:
                            print(f"Error sending to client: {e}")
                            dead_clients.add(client)
                    clients.difference_update(dead_clients)
                except Exception as e:
                    print(f"Error in loop: {e}")
                    break
    except Exception as e:
        print(f"WebSocket connection error: {e}")
    finally:
        print("Camera connection closed")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=3000)