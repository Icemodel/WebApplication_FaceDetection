import cv2
import numpy as np
import asyncio
import websockets

cap = cv2.VideoCapture(0)
frame_queue = asyncio.Queue(maxsize=1)

async def receive_processed(websocket):
    frame_count = 0
    while True:
        try:
            processed_frame_bytes = await websocket.recv()
            print(f"[Recv] Received processed frame {frame_count}, size: {len(processed_frame_bytes)} bytes")
            # ถ้า queue เต็ม ให้ลบ frame เก่าออกก่อน
            while frame_queue.full():
                try:
                    frame_queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
            await frame_queue.put(processed_frame_bytes)
            frame_count += 1
        except Exception as e:
            print(f"[Recv] Exception: {e}")
            break

async def main():
    last_frame = None  # เก็บ processed frame ล่าสุด
    try:
        async with websockets.connect("ws://localhost:3000/ws/camera") as websocket:
            print("Connected to WebSocket!")
            recv_task = asyncio.create_task(receive_processed(websocket))
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("Camera read failed, breaking loop")
                    break

                # ส่งภาพดิบไป server
                _, buffer = cv2.imencode(".jpg", frame)
                frame_bytes = buffer.tobytes()
                await websocket.send(frame_bytes)
                frame_count += 1

                # แสดงผล processed frame ล่าสุดจาก queue (ถ้ามี)
                try:
                    while frame_queue.qsize() > 1:
                        frame_queue.get_nowait()
                    processed_frame_bytes = frame_queue.get_nowait()
                    processed_frame_array = np.frombuffer(processed_frame_bytes, dtype=np.uint8)
                    processed_frame = cv2.imdecode(processed_frame_array, cv2.IMREAD_COLOR)
                    if processed_frame is not None:
                        last_frame = processed_frame
                    else:
                        print("[Main] Warning: processed_frame is None after decode!")
                except asyncio.QueueEmpty:
                    pass

                # แสดงผล frame ล่าสุด (ถ้ามี)
                if last_frame is not None:
                    cv2.imshow("Host Camera - YOLO Detection (Processed Frame)", last_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Quit pressed, breaking loop")
                    break

                await asyncio.sleep(0.01)  # sleep สั้นเพื่อให้แสดงผลลื่นขึ้น

            await recv_task
    except Exception as e:
        print(f"Exception in main: {e}")
    finally:
        print("Releasing camera and closing windows")
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())