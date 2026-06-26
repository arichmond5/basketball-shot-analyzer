from fastapi import APIRouter, UploadFile, File
from .angles import compute_angles
from .phases import find_phases
import cv2
import os
import mediapipe as mp

UPLOAD_DIR = "videos"
OUTPUT_DIR = "overlays"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

LM = {
    "left_shoulder":  11, "right_shoulder": 12,
    "left_elbow":     13, "right_elbow":    14,
    "left_wrist":     15, "right_wrist":    16,
    "left_index":     19, "right_index":    20,
    "left_hip":       23, "right_hip":      24,
    "left_knee":      25, "right_knee":     26,
    "left_ankle":     27, "right_ankle":    28,
}

CONNECTIONS = [
    ("right_shoulder","right_elbow"), ("right_elbow","right_wrist"),
    ("left_shoulder", "left_elbow"),  ("left_elbow", "left_wrist"),
    ("right_shoulder","left_shoulder"),
    ("right_shoulder","right_hip"),   ("left_shoulder","left_hip"),
    ("right_hip","left_hip"),
    ("right_hip","right_knee"),       ("right_knee","right_ankle"),
    ("left_hip", "left_knee"),        ("left_knee", "left_ankle"),
]


def analyze_video(file_id: str, file_path: str) -> dict:

    output_path = os.path.join(OUTPUT_DIR, f"{file_id}_overlay.mp4")

    # 1. MediaPipe imports
    BaseOptions           = mp.tasks.BaseOptions
    PoseLandmarker        = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    VisionRunningMode     = mp.tasks.vision.RunningMode

    # 2. Setup model
    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path="assets/pose_landmarker.task"),
        running_mode=VisionRunningMode.VIDEO
    )

    # 3. Open video
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        return {"error": "Could not open video"}

    fps    = cap.get(cv2.CAP_PROP_FPS) or 30
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"avc1"),
        fps,
        (width, height),
    )

    frame_idx    = 0
    frame_data = []

    # 4. Run pose detection
    with PoseLandmarker.create_from_options(options) as landmarker:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame    = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image     = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            timestamp_ms = int(frame_idx * (1000 / fps))
            result       = landmarker.detect_for_video(mp_image, timestamp_ms)

            if result.pose_landmarks:
                landmarks = result.pose_landmarks[0]

                # Draw dots on the frame
                landmarks_dict = {}
                for name, idx in LM.items():
                    lm = landmarks[idx]
                    if lm.visibility > 0.7:
                        x, y = int(lm.x * width), int(lm.y * height)
                        cv2.circle(frame, (x, y), 8, (0, 255, 0),   -1, cv2.LINE_AA)
                        cv2.circle(frame, (x, y), 8, (0, 150, 255),  2, cv2.LINE_AA)
                        cv2.putText(frame, name, (x + 6, y - 6), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.4, (0, 255, 0), 1, cv2.LINE_AA)
                        landmarks_dict = { "x": lm.x, "y": lm.y, "z": lm.z, "visibility": lm.visibility }

                    frame_data.append({
                        "frame_index": frame_idx,
                        "landmarks": landmarks_dict,
                        "frame": frame.copy()
                    })

                for start_name, end_name in CONNECTIONS:
                    idx1      = LM[start_name]
                    idx2      = LM[end_name]
                    lm1, lm2  = landmarks[idx1], landmarks[idx2]
                    if lm1.visibility > 0.7 and lm2.visibility > 0.7:
                        x1, y1 = int(lm1.x * width), int(lm1.y * height)
                        x2, y2 = int(lm2.x * width), int(lm2.y * height)
                        cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

            writer.write(frame)
            frame_idx += 1

    cap.release()
    writer.release()

    frame_data = compute_angles(frame_data)
    key_frames = find_phases(frame_data)

    for phase, idx in key_frames.items():
        cv2.imwrite(f"overlays/{file_id}_{phase}.jpg", frame_data[idx]["frame"])

    return {
        "frames_processed": frame_idx,
        "output_video":     output_path,
        "key_frames":       {phase: f"overlays/{file_id}_{phase}.jpg" for phase in key_frames},
    }