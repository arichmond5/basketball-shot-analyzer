import cv2
import json
import os
import mediapipe as mp


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


def render_overlay(file_id: str, video_path: str, data_path: str, output_path: str):

    with open(data_path, "r") as f:
        frame_data = json.load(f)

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = cv2.VideoWriter(
        output_path,
        cv2.VideoWriter_fourcc(*"avc1"),
        fps,
        (width, height),
    )

    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx < len(frame_data):
            data = frame_data[frame_idx]
            landmarks = data["landmarks"]

            # draw joints
            for name, lm in landmarks.items():
                x = int(lm["x"] * width)
                y = int(lm["y"] * height)

                cv2.circle(frame, (x, y), 6, (0, 255, 0), -1)
                cv2.putText(frame, name, (x+5, y-5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4,
                            (0, 255, 0), 1)

            # draw skeleton
            for start, end in CONNECTIONS:
                if start in landmarks and end in landmarks:
                    lm1 = landmarks[start]
                    lm2 = landmarks[end]

                    x1, y1 = int(lm1["x"] * width), int(lm1["y"] * height)
                    x2, y2 = int(lm2["x"] * width), int(lm2["y"] * height)

                    cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

        writer.write(frame)
        frame_idx += 1

    cap.release()
    writer.release()

    return output_path