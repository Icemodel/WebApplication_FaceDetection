import cv2
import numpy as np
import torch
import dlib
import sys
import os
import psycopg2
from deepface import DeepFace
from services.face_detection import detect_faces

# --- Database and Model Setup ---
# ส่วนนี้มาจาก face_recognition.py
try:
    conn = psycopg2.connect(dbname="projectDatabase", user="postgres", password="54375437", host="localhost")
    cursor = conn.cursor()
    print("Database connection successful.")
except Exception as e:
    print(f"Database connection failed: {e}")
    conn, cursor = None, None

# --- Global State for Face Processing ---
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU name:", torch.cuda.get_device_name(0))

last_recognized_faces = {}
tracker_id_count = 0

# --- Helper Functions ---
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

# --- Face Recognition Function (Integrated from face_recognition.py) ---
def recognize_face(face_crop, threshold=0.6):
    """
    ฟังก์ชันนี้จะแปลงภาพใบหน้าที่ตัดมาเป็น vector,
    ค้นหาในฐานข้อมูล, และคืนค่าชื่อกับ embedding vector.
    """
    if not conn or not cursor:
        print("[recognize_face] No database connection.")
        return "DB Error", None

    try:
        embedding_vector = DeepFace.represent(face_crop, model_name="Facenet", enforce_detection=False)
        if isinstance(embedding_vector, list) and len(embedding_vector) > 0:
            embedding_vector = embedding_vector[0]
        
        embedding_vector = np.array(embedding_vector["embedding"], dtype=np.float32)
        embedding_str = "[" + ",".join([str(x) for x in embedding_vector.tolist()]) + "]"

        # Query vector ที่ใกล้สุด
        query = """
            SELECT faces.id, faces.person_id, person.name, faces.embedding
            FROM faces
            JOIN person ON faces.person_id = person.id
            ORDER BY faces.embedding <-> %s::vector
            LIMIT 1;
        """
        cursor.execute(query, (embedding_str,))
        result = cursor.fetchone()
        conn.commit()

        print("[recognize_face] DB result:", result)
        if result:
            db_embedding = np.array(eval(result[3]), dtype=np.float32)
            similarity = np.dot(embedding_vector, db_embedding) / (np.linalg.norm(embedding_vector) * np.linalg.norm(db_embedding))
            print(f"[recognize_face] similarity: {similarity:.3f}")
            if similarity > threshold:
                return result[2], embedding_vector
            else:
                return "Unknown", embedding_vector
        else:
            return "Unknown", embedding_vector
            
    except Exception as e:
        print(f"[recognize_face] Recognition error: {e}")
        conn.rollback()
        return "Error", None

# --- Main Frame Processing Logic ---
async def process_frame_logic(frame_bytes: bytes) -> bytes:
    """
    ฟังก์ชันหลักในการประมวลผลใบหน้าในแต่ละเฟรม
    """
    global last_recognized_faces
    frame_array = np.frombuffer(frame_bytes, dtype=np.uint8)
    frame = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

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

    # 2. Detect new faces
    detected_faces = detect_faces(frame)
    for (x1, y1, x2, y2) in detected_faces:
        if not any(iou((x1, y1, x2, y2), data['bbox']) > 0.5 for data in last_recognized_faces.values()):
            face_crop = frame[y1:y2, x1:x2]
            
            # เรียกใช้ฟังก์ชัน recognize_face ที่อยู่ในไฟล์เดียวกันนี้
            name, embedding = recognize_face(face_crop)
            
            if embedding is not None: # เพิ่มการตรวจสอบว่าการ recognition สำเร็จหรือไม่
                tracker = dlib.correlation_tracker()
                tracker.start_track(frame, dlib.rectangle(x1, y1, x2, y2))
                face_id = get_new_face_id()
                last_recognized_faces[face_id] = {'name': name, 'embedding': embedding, 'tracker': tracker, 'bbox': (x1, y1, x2, y2)}

    # 3. Draw results
    for data in last_recognized_faces.values():
        x1, y1, x2, y2 = data['bbox']
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, str(data['name']), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    ret, buffer = cv2.imencode(".jpg", frame)
    return buffer.tobytes() if ret else b''