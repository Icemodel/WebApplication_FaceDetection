import cv2
import numpy as np
from deepface import DeepFace
import psycopg2

#กรอกข้อมูลเอง person_id และ path ของภาพที่ต้องการเก็บ
person_id = 1 
img_path = "C:/Users/Icemo/Desktop/Studies/Fast API/photos/T8.jpg"
img = cv2.imread(img_path)

# 2. แปลงภาพเป็น embedding vector
embedding_obj = DeepFace.represent(img, model_name="Facenet", enforce_detection=False)
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