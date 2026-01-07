import cv2
import os
import numpy as np

# Thư mục chứa ảnh khuôn mặt
data_path = 'dataset'
faces = []
labels = []

# Duyệt qua các thư mục con (mỗi người một thư mục)
for person_id, person_name in enumerate(os.listdir(data_path)):
    person_folder = os.path.join(data_path, person_name)
    if not os.path.isdir(person_folder):
        continue
    print(f"Đang đọc ảnh của: {person_name}")

    for file in os.listdir(person_folder):
        img_path = os.path.join(person_folder, file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        faces.append(img)
        labels.append(person_id)

# Chuyển sang định dạng numpy array
faces = np.array(faces)
labels = np.array(labels)

# Khởi tạo bộ nhận diện LBPH
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Huấn luyện mô hình
print("Bắt đầu huấn luyện mô hình...")
recognizer.train(faces, labels)
print("✅ Huấn luyện xong!")

# Lưu lại mô hình
recognizer.save('face_trained.yml')
print("💾 Đã lưu model vào file face_trained.yml")
