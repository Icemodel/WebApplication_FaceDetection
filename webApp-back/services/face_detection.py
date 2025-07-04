
#YOLO
from ultralytics import YOLO

yolo_model = YOLO("C:/Users/Icemo/Desktop/Studies/Fast API/weights/yolov8n-face.pt")
print("YOLOv8 loaded successfully!")

def detect_faces(frame):
    results = yolo_model(frame)
    faces = []

    for box in results[0].boxes.xyxy:
        x1, y1, x2, y2 = map(int, box)
        faces.append((x1, y1, x2, y2))

    return faces


'''
#Mediapipe
import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=10, refine_landmarks=True, min_detection_confidence=0.6)

def detect_faces(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    faces = []
    h, w, _ = frame.shape
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # หาค่า min/max ของจุด landmark เพื่อสร้าง bounding box
            x_coords = [lm.x for lm in face_landmarks.landmark]
            y_coords = [lm.y for lm in face_landmarks.landmark]
            x1 = int(min(x_coords) * w)
            y1 = int(min(y_coords) * h)
            x2 = int(max(x_coords) * w)
            y2 = int(max(y_coords) * h)
            # ตรวจสอบขอบเขต
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            faces.append((x1, y1, x2, y2))
    return faces
'''


