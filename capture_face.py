import cv2
import os

# Nạp bộ cascade nhận diện khuôn mặt
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
output_folder = "thanh"

# Mở camera
cap = cv2.VideoCapture(0)
frame_num = 0
color = (0, 255, 0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        
        out_frame = frame[x:x+h, y:y+h]
        # Save each frame as a JPEG file
        filename = os.path.join(output_folder, f"{frame_num}.jpg")
        cv2.imwrite(filename, out_frame)
        frame_num += 1
        
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

    cv2.imshow('Face Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
