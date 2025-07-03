import cv2
from face_detection import detect_faces

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    faces = detect_faces(frame)
    print("Detected faces:", faces)

    # วาดกรอบใบหน้าทุกใบหน้าที่ตรวจจับได้
    for (x1, y1, x2, y2) in faces:
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Test Camera", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()