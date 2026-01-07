**Hệ Thống Nhận Diện Khuôn Mặt Điều Khiển Cửa (Raspberry Pi & ESP) tích hợp AI, IoT 

📌 Các tính năng chính
Thu thập dữ liệu: Tự động chụp và lưu trữ ảnh khuôn mặt từ Camera.

Huấn luyện: Tạo mô hình nhận diện cá nhân hóa dựa trên dữ liệu ảnh đã chụp.

Nhận diện thời gian thực: Nhận diện người dùng với độ chính xác cao và xử lý logic đóng/mở cửa.

Tương tác phần cứng: Giao tiếp giữa RPi và ESP để xác thực trạng thái vật lý.

📂 Cấu trúc mã nguồn
capture_face.py: Chụp ảnh gương mặt từ webcam/camera và lưu vào thư mục để làm dữ liệu huấn luyện.

train_faces.py: Đọc các ảnh từ thư mục dataset, huấn luyện bộ nhận diện LBPH và xuất ra file face_trained.yml.

face_recognition.py: File thực thi chính. Nhận diện khuôn mặt, kiểm tra tín hiệu từ ESP (Pin 17) và phản hồi lệnh mở cửa (Pin 27).

🛠 Yêu cầu hệ thống
1. Phần cứng
Raspberry Pi (đã cài đặt OS).

Camera USB hoặc Raspberry Pi Camera.

Kết nối dây giữa RPi và ESP.

2. Phần mềm & Thư viện
Cài đặt các thư viện cần thiết bằng lệnh sau:

Bash

pip install opencv-python opencv-contrib-python numpy RPi.GPIO
🔌 Cấu hình chân GPIO (Raspberry Pi)
Hệ thống sử dụng sơ đồ chân BCM: | Chân (Pin) | Vai trò | Chức năng | |:---:|:---:|:---| | GPIO 17 | INPUT | Nhận tín hiệu từ ESP (phát hiện người đến gần). | | GPIO 27 | OUTPUT | Gửi tín hiệu phản hồi cho ESP (mở cửa khi đúng người). |

🚀 Hướng dẫn vận hành
Bước 1: Thu thập dữ liệu
Chạy script để chụp ảnh gương mặt của bạn (nhấn 'q' để dừng):

Bash

python capture_face.py
Ảnh sẽ được lưu vào thư mục thanh dưới định dạng .jpg.

Bước 2: Huấn luyện mô hình
Chạy lệnh sau để hệ thống học các khuôn mặt trong thư mục dataset:

Bash

python train_faces.py
Kết quả sẽ là file face_trained.yml dùng cho việc nhận diện.

Bước 3: Chạy chương trình nhận diện
Bắt đầu chế độ bảo mật:

Bash

python face_recognition.py
Mở cửa: Khi nhận diện đúng (độ tin cậy < 40) và có tín hiệu từ chân 17, chân 27 sẽ lên mức HIGH.

Đóng cửa: Sau 10 giây kể từ khi mở, chân 27 sẽ tự động về mức LOW.
