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
                    print("[Recv] Dropped old frame from queue")
                except asyncio.QueueEmpty:
                    break
            await frame_queue.put(processed_frame_bytes)
            print(f"[Recv] Put processed frame {frame_count} to queue (qsize={frame_queue.qsize()})")
            frame_count += 1
        except Exception as e:
            print(f"[Recv] Exception: {e}")
            break

async def main():
    last_frame = None  # เก็บ processed frame ล่าสุด
    try:
        print("[Main] Starting camera client...")
        async with websockets.connect("ws://127.0.0.1:3001/ws/camera") as websocket:
            print("[Main] Connected to WebSocket!")
            recv_task = asyncio.create_task(receive_processed(websocket))
            frame_count = 0
            while True:
                print(f"[Main] Reading frame {frame_count} from camera...")
                ret, frame = cap.read()
                if not ret:
                    print("[Main] Camera read failed, breaking loop")
                    break

                # ส่งภาพดิบไป server
                _, buffer = cv2.imencode(".jpg", frame)
                frame_bytes = buffer.tobytes()
                await websocket.send(frame_bytes)
                print(f"[Main] Sent frame {frame_count}, size: {len(frame_bytes)} bytes")
                frame_count += 1

                # แสดงผล processed frame ล่าสุดจาก queue (ถ้ามี)
                try:
                    print(f"[Main] Queue size before get: {frame_queue.qsize()}")
                    while frame_queue.qsize() > 1:
                        frame_queue.get_nowait()
                        print("[Main] Dropped old frame from queue (main loop)")
                    processed_frame_bytes = frame_queue.get_nowait()
                    print(f"[Main] Got processed frame from queue, size: {len(processed_frame_bytes)} bytes")
                    processed_frame_array = np.frombuffer(processed_frame_bytes, dtype=np.uint8)
                    processed_frame = cv2.imdecode(processed_frame_array, cv2.IMREAD_COLOR)
                    if processed_frame is not None:
                        last_frame = processed_frame
                        print("[Main] Decoded processed frame successfully")
                    else:
                        print("[Main] Warning: processed_frame is None after decode!")
                except asyncio.QueueEmpty:
                    print("[Main] QueueEmpty (no processed frame yet)")
                    pass

                # แสดงผล frame ล่าสุด (ถ้ามี)
                if last_frame is not None:
                    cv2.imshow("Host Camera - YOLO Detection (Processed Frame)", last_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("[Main] Quit pressed, breaking loop")
                    break

                await asyncio.sleep(0.01)  # sleep สั้นเพื่อให้แสดงผลลื่นขึ้น

            await recv_task
    except Exception as e:
        print(f"[Main] Exception in main: {e}")
    finally:
        print("[Main] Releasing camera and closing windows")
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())