import cv2
import os
import RPi.GPIO as GPIO
import time



PIN_FROM_ESP = 17  # ESP gửi tín hiệu “đến gần”
PIN_TO_ESP = 27    # RPi phản hồi “đúng người”

#Cấu hình cho các chân 

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_FROM_ESP, GPIO.IN)
GPIO.setup(PIN_TO_ESP, GPIO.OUT)
GPIO.output(PIN_TO_ESP, GPIO.LOW)

# Nạp bộ cascade nhận diện khuôn mặt
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Nạp model đã huấn luyện
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('face_trained.yml')

# Danh sách tên người (phải đúng thứ tự như khi train)
labels = os.listdir('/home/thanh/Face_Recognition/dataset')



# Mở camera
cap = cv2.VideoCapture(0)
authentication_wait = 10
start_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    time_elapsed = time.time() - start_time
    # print("time_elapsed", time_elapsed, "start_time", start_time)
    if start_time > 0 and time_elapsed >= authentication_wait:
        GPIO.output(PIN_TO_ESP, GPIO.LOW)
        start_time = 0
        print("time over, close door")

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        id_, confidence = recognizer.predict(face_roi)

        if confidence < 40:  # confidence càng nhỏ càng chính xác
            name = labels[id_]
            color = (0, 255, 0)
            label = f"{name} ({round(100 - confidence, 1)}%)"
            
            signal = GPIO.input(PIN_FROM_ESP)
            if signal == GPIO.HIGH:
                start_time = time.time()
                GPIO.output(PIN_TO_ESP, GPIO.HIGH)
            print("open door", start_time)
        else:
            name = "Unknown, confidence = " + str(100 - confidence)
            color = (0, 0, 255)
            label = name
            

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow('Face Recognition', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
GPIO.cleanup()
cv2.destroyAllWindows()
