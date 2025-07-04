import numpy as np
import psycopg2
from deepface import DeepFace

conn = psycopg2.connect(dbname="projectDatabase", user="postgres", password="54375437", host="localhost")
cursor = conn.cursor()

def recognize_face(face_crop, threshold=0.6):
    try:
        embedding_vector = DeepFace.represent(face_crop, model_name="Facenet", enforce_detection=False)
        if isinstance(embedding_vector, list):
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
            db_embedding = np.array(eval(result[3]), dtype=np.float32)  # สมมติว่าเก็บเป็น string vector
            # คำนวณ cosine similarity
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
        return "Unknown", None