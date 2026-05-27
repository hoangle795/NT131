import cv2
import requests
import time

SERVER_URL = "http://34.46.198.182:8000/upload"  # Địa chỉ server FastAPI

def send_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Không thể mở camera!")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        _, img_encoded = cv2.imencode('.jpg', frame)
        try:
            response = requests.post(
                SERVER_URL,
                files={'file': img_encoded.tobytes()},
                timeout=2
            )
            if response.status_code == 200:
                print("✅ Frame sent.")
            else:
                print(f"⚠️ Lỗi gửi frame. Status: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Lỗi kết nối: {e}")

        time.sleep(0.05)

    cap.release()

if __name__ == "__main__":
    send_camera()
