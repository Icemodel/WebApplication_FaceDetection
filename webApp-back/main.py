import cv2
import numpy as np
import websockets
import asyncio
import torch
import dlib
from services.face_detection import detect_faces
from services.face_recognition import recognize_face

print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU name:", torch.cuda.get_device_name(0))

last_recognized_faces = {}  # {face_id: {'name':..., 'embedding':..., 'tracker':..., 'bbox':(x1,y1,x2,y2)}}
tracker_id_count = 0

def get_new_face_id():
    global tracker_id_count
    tracker_id_count += 1
    return f"face_{tracker_id_count}"

def iou(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    iou = interArea / float(boxAArea + boxBArea - interArea + 1e-6)
    return iou

async def process_frame(websocket, path):
    print(f"Accepted connection from: {path}")
    global last_recognized_faces
    while True:
        frame_bytes = await websocket.recv()
        frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
        frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

        # 1. อัปเดตตำแหน่งใบหน้าด้วย dlib tracker
        to_remove = []
        for face_id, data in last_recognized_faces.items():
            tracker = data['tracker']
            tracking_quality = tracker.update(frame)
            pos = tracker.get_position()
            x1 = int(pos.left())
            y1 = int(pos.top())
            x2 = int(pos.right())
            y2 = int(pos.bottom())
            if tracking_quality < 7 or x1 < 0 or y1 < 0 or x2 > frame.shape[1] or y2 > frame.shape[0]:
                to_remove.append(face_id)
            else:
                data['bbox'] = (x1, y1, x2, y2)
        for fid in to_remove:
            del last_recognized_faces[fid]

        IOU_THRESHOLD = 0.5

        # 2. ตรวจจับใบหน้าใหม่ด้วย YOLO
        detected_faces = detect_faces(frame)
        for (x1, y1, x2, y2) in detected_faces:
            max_iou = 0
            matched_id = None
            for face_id, data in last_recognized_faces.items():
                iou_val = iou((x1, y1, x2, y2), data['bbox'])
                if iou_val > max_iou:
                    max_iou = iou_val
                    matched_id = face_id
            if max_iou > IOU_THRESHOLD:
                continue  # มี tracker แล้ว

            # เป็นใบหน้าใหม่ → ทำ Face Recognition + Query Database
            face_crop = frame[y1:y2, x1:x2]
            print("ก่อนเรียก recognize_face")
            name, embedding = recognize_face(face_crop)
            print("หลังเรียก recognize_face")
            print(f"[server] Recognized: {name}")
            tracker = dlib.correlation_tracker()
            tracker.start_track(frame, dlib.rectangle(x1, y1, x2, y2))
            face_id = get_new_face_id()
            last_recognized_faces[face_id] = {
                'name': name,
                'embedding': embedding,
                'tracker': tracker,
                'bbox': (x1, y1, x2, y2)
            }

        # 3. วาดกรอบและชื่อ (ใช้ cache ที่ recognize แล้ว)
        for data in last_recognized_faces.values():
            x1, y1, x2, y2 = data['bbox']
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, str(data['name']), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        ret, buffer = cv2.imencode(".jpg", frame)
        if ret:
            await websocket.send(buffer.tobytes())

async def server():
    async with websockets.serve(process_frame, "127.0.0.1", 9000):
        print("WebSocket server started at ws://127.0.0.1:9000")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(server())
    