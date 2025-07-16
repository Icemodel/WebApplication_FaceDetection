import cv2
import numpy as np
import asyncio
import websockets

async def main():
    cap = cv2.VideoCapture(0)
    async with websockets.connect("ws://127.0.0.1:3002") as websocket:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Camera read failed")
                break

            # ส่ง frame เต็มไปยัง server
            _, buffer = cv2.imencode(".jpg", frame)
            await websocket.send(buffer.tobytes())

            # รับ processed frame กลับมา
            processed_bytes = await websocket.recv()
            processed_array = np.frombuffer(processed_bytes, dtype=np.uint8)
            processed_frame = cv2.imdecode(processed_array, cv2.IMREAD_COLOR)
            if processed_frame is not None:
                cv2.imshow("Face Recognition Result", processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quit pressed, breaking loop")
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())