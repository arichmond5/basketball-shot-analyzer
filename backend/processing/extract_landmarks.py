import cv2
import mediapipe as mp

LM = {
    "left_shoulder":  11, "right_shoulder": 12,
    "left_elbow":     13, "right_elbow":    14,
    "left_wrist":     15, "right_wrist":    16,
    "left_pinky":     17, "right_pinky":    18,
    "left_hip":       23, "right_hip":      24,
    "left_knee":      25, "right_knee":     26,
    "left_ankle":     27, "right_ankle":    28,
}

def analyze_video(file_path: str) -> list[dict]:

    BaseOptions           = mp.tasks.BaseOptions
    PoseLandmarker        = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    VisionRunningMode     = mp.tasks.vision.RunningMode

    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path="assets/pose_landmarker.task"),
        running_mode=VisionRunningMode.VIDEO
    )

    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        return []

    fps        = cap.get(cv2.CAP_PROP_FPS) or 30
    frame_idx  = 0
    frame_data = []

    with PoseLandmarker.create_from_options(options) as landmarker:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb          = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image     = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
            timestamp_ms = int(frame_idx * (1000 / fps))
            result       = landmarker.detect_for_video(mp_image, timestamp_ms)

            if result.pose_landmarks:
                landmarks      = result.pose_landmarks[0]
                landmarks_dict = {}

                for name, idx in LM.items():
                    lm = landmarks[idx]
                    landmarks_dict[name] = {
                        "x":          lm.x,
                        "y":          lm.y,
                        "z":          lm.z,
                        "visibility": lm.visibility
                    }

                frame_data.append({
                    "frame_index": frame_idx,
                    "landmarks":   landmarks_dict,
                })

            frame_idx += 1

    cap.release()
    return frame_data