import cv2
import numpy as np
import torch
import dlib
from deepface import DeepFace
from services.face_detection import detect_faces
import concurrent.futures
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import FaceDB, PersonDB  
 

# ตรวจสอบการ์ดจอว่าใช้ CUDA ได้หรือไม่
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU name:", torch.cuda.get_device_name(0))

last_recognized_faces = {}
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
    iou_val = interArea / float(boxAArea + boxBArea - interArea + 1e-6)
    return iou_val

async def recognize_face(face_crop, db: AsyncSession, threshold=0.6):
    """
    ฟังก์ชันนี้จะแปลงภาพใบหน้าที่ตัดมาเป็น vector,
    ค้นหาในฐานข้อมูลด้วย SQLAlchemy ORM, และคืนค่าชื่อกับ embedding vector.
    """
    try:
        embedding_vector = DeepFace.represent(face_crop, model_name="Facenet", enforce_detection=False)
        if isinstance(embedding_vector, list) and len(embedding_vector) > 0:
            embedding_vector = embedding_vector[0]
        embedding_vector = np.array(embedding_vector["embedding"], dtype=np.float32)

        # ดึง face ทั้งหมดในฐานข้อมูล (หรือปรับ query ให้เหมาะสมกับการใช้งานจริง)
        result = await db.execute(
            select(FaceDB, PersonDB)
            .join(PersonDB, FaceDB.person_id == PersonDB.id)
        )
        faces = result.all()

        # หา face ที่คล้ายที่สุด
        best_similarity = -1
        best_name = "Unknown"
        for face, person in faces:
            db_embedding = np.array(face.embedding, dtype=np.float32)
            similarity = np.dot(embedding_vector, db_embedding) / (np.linalg.norm(embedding_vector) * np.linalg.norm(db_embedding))
            if similarity > best_similarity:
                best_similarity = similarity
                best_name = person.name

        if best_similarity > threshold:
            return best_name, embedding_vector
        else:
            return "Unknown", embedding_vector

    except Exception as e:
        print(f"[recognize_face_orm] Recognition error: {e}")
        return "Error", None

DETECT_INTERVAL = 5  # ตรวจจับใบหน้าใหม่ทุก x เฟรม
frame_counter = 0

executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

async def process_frame(frame_bytes: bytes, db: AsyncSession) -> bytes:
    global last_recognized_faces, frame_counter
    frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
    frame_counter += 1

    loop = asyncio.get_running_loop()

    # 1. Update trackers
    to_remove = []
    for face_id, data in last_recognized_faces.items():
        tracker = data['tracker']
        if tracker.update(frame) < 7:
            to_remove.append(face_id)
        else:
            pos = tracker.get_position()
            data['bbox'] = (int(pos.left()), int(pos.top()), int(pos.right()), int(pos.bottom()))
    for fid in to_remove:
        del last_recognized_faces[fid]

    # 2. ตรวจจับใบหน้าใหม่ (ตามที่กำหนด DETECT_INTERVAL เอาไว้)
    if frame_counter % DETECT_INTERVAL == 0:
        detected_faces = await loop.run_in_executor(executor, detect_faces, frame)
        for (x1, y1, x2, y2) in detected_faces:
            is_duplicate = False
            for data in last_recognized_faces.values():
                iou_val = iou((x1, y1, x2, y2), data['bbox'])
                if iou_val > 0.3:
                    is_duplicate = True
                    break
            if is_duplicate:
                continue

            face_crop = frame[y1:y2, x1:x2]
            try:
                face_crop = cv2.resize(face_crop, (160, 160))
            except Exception:
                continue
            name, embedding = await recognize_face(face_crop, db)
            if embedding is not None:
                tracker = dlib.correlation_tracker()
                tracker.start_track(frame, dlib.rectangle(x1, y1, x2, y2))
                face_id = get_new_face_id()
                last_recognized_faces[face_id] = {
                    'name': name,
                    'embedding': embedding,
                    'tracker': tracker,
                    'bbox': (x1, y1, x2, y2)
                }

    # 3. Draw results
    print(f"[DEBUG] frame_counter={frame_counter} | trackers={len(last_recognized_faces)}")
    for face_id, data in last_recognized_faces.items():
        x1, y1, x2, y2 = data['bbox']
        print(f"[DEBUG] Drawing box for face_id={face_id} at ({x1},{y1},{x2},{y2}) name={data['name']}")
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, str(data['name']), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    ret, buffer = cv2.imencode(".jpg", frame)
    return buffer.tobytes() if ret else b''