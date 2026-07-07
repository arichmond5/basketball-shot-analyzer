"""
Detects shooting side based on visibility of landmarks.
"""

def detect_shooting_side(frame_data: list[dict]) -> str:
    left_total  = 0.0
    right_total = 0.0
    count       = 0

    for frame in frame_data:
        landmarks = frame["landmarks"]

        left_total += (
            landmarks["left_wrist"]["visibility"] +
            landmarks["left_elbow"]["visibility"] +
            landmarks["left_shoulder"]["visibility"] +
            landmarks["left_hip"]["visibility"] +
            landmarks["left_knee"]["visibility"] +
            landmarks["left_ankle"]["visibility"]
        )
        right_total += (
            landmarks["right_wrist"]["visibility"] +
            landmarks["right_elbow"]["visibility"] +
            landmarks["right_shoulder"]["visibility"] +
            landmarks["right_hip"]["visibility"] +
            landmarks["right_knee"]["visibility"] +
            landmarks["right_ankle"]["visibility"]
        )
        count += 1

    if count == 0:
        return "right"

    return "right" if right_total >= left_total else "left"