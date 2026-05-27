from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import mediapipe as mp

app = FastAPI()

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        np_arr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        fall_detected = detect_fall(image)

        return JSONResponse(content={"fall_detected": fall_detected})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def detect_fall(image, fall_threshold=0.25, velocity_threshold=0.1, frame_history=5):
    # Khởi tạo biến lưu trữ lịch sử vị trí
    if not hasattr(detect_fall, 'history'):
        detect_fall.history = []
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)
    
    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark
        
        try:
            # Lấy các điểm mốc quan trọng
            left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            left_hip = lm[mp_pose.PoseLandmark.LEFT_HIP]
            right_hip = lm[mp_pose.PoseLandmark.RIGHT_HIP]
            left_ankle = lm[mp_pose.PoseLandmark.LEFT_ANKLE]
            right_ankle = lm[mp_pose.PoseLandmark.RIGHT_ANKLE]
            
            # Tính toán trung bình cho các cặp điểm đối xứng
            shoulder_y = (left_shoulder.y + right_shoulder.y) / 2
            hip_y = (left_hip.y + right_hip.y) / 2
            ankle_y = (left_ankle.y + right_ankle.y) / 2
            
            # Tính chiều cao cơ thể dựa trên khung xương
            vertical_span = abs(ankle_y - shoulder_y)
            
            # Kiểm tra 1: Tỷ lệ chiều cao (nằm ngang)
            height_ratio_condition = vertical_span < fall_threshold
            
            # Kiểm tra 2: Góc nghiêng của cơ thể
            # Tính góc giữa vai và hông
            shoulder_hip_angle = abs(left_shoulder.x - right_shoulder.x) / abs(left_hip.x - right_hip.x)
            angle_condition = shoulder_hip_angle > 2.0  # Ngưỡng góc nghiêng
            
            # Kiểm tra 3: Tốc độ thay đổi tư thế (đột ngột)
            current_position = (shoulder_y, hip_y, ankle_y)
            detect_fall.history.append(current_position)
            
            if len(detect_fall.history) > frame_history:
                # Tính tốc độ thay đổi vị trí
                prev_position = detect_fall.history[-frame_history]
                velocity = abs(current_position[0] - prev_position[0]) / frame_history
                velocity_condition = velocity > velocity_threshold
                
                # Giữ kích thước lịch sử ổn định
                if len(detect_fall.history) > frame_history * 2:
                    detect_fall.history.pop(0)
            else:
                velocity_condition = False
            
            # Kết hợp các điều kiện
            if height_ratio_condition and (angle_condition or velocity_condition):
                return True
            
        except Exception as e:
            print(f"Error in pose estimation: {e}")
            pass
    
    return False
