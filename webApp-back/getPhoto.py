import cv2
import numpy as np
from deepface import DeepFace
import psycopg2
from services.face_detection import detect_faces  # ต้องมีฟังก์ชันนี้ในโปรเจกต์

# กรอกข้อมูลเอง person_id และ path ของภาพที่ต้องการเก็บ
person_id = int(input("Enter person_id: "))
name = input("Enter image name: ")
img_path = f"C:/Users/Icemo/Desktop/Studies/webApplication-FaceDetection/webApp-back/src/assets/faces/{name}.jpg"
img = cv2.imread(img_path)

# 1. ตรวจจับใบหน้าด้วย YOLO และ crop เฉพาะใบหน้าแรกที่เจอ
faces = detect_faces(img)  # [(x1, y1, x2, y2), ...]
if not faces:
    print("Face not detected!")
    exit()
x1, y1, x2, y2 = faces[0]
face_crop = img[y1:y2, x1:x2]

# 2. แปลงภาพเป็น embedding vector
embedding_obj = DeepFace.represent(face_crop, model_name="Facenet", enforce_detection=False)
if isinstance(embedding_obj, list):
    embedding_obj = embedding_obj[0]
embedding_vector = np.array(embedding_obj["embedding"], dtype=np.float32).tolist()

# 3. แปลงเป็น string สำหรับ pgvector
embedding_str = "[" + ",".join([str(x) for x in embedding_vector]) + "]"

# 4. เก็บลง database
conn = psycopg2.connect(dbname="projectDatabase", user="postgres", password="54375437", host="localhost")
cursor = conn.cursor()

query = "INSERT INTO faces (person_id, embedding) VALUES (%s, %s::vector)"
cursor.execute(query, (person_id, embedding_str))
conn.commit()
cursor.close()
conn.close()
print("Insert success!")