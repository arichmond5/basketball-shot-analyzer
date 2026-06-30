import numpy as np

VISIBILITY_THRESHOLD = 0.75

def compute_angle(a, b, c) -> float:
    """Interior angle at B in the A-B-C triplet, degrees [0, 180]."""
    a, b, c = np.array(a), np.array(b), np.array(c)

    ba = a - b
    bc = c - b

    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-9)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)

    return float(np.degrees(np.arccos(cos_angle)))

def lm_to_point(lm_dict: dict) -> list[float]:
    return [lm_dict["x"], lm_dict["y"]]

def visible(lm_dict: dict) -> bool:
    return lm_dict["visibility"] >= VISIBILITY_THRESHOLD

def compute_trunk_lean(shoulder: dict, hip: dict) -> float:
    """Degrees of forward lean from vertical. 0 = upright, higher = more lean."""
    dx = shoulder["x"] - hip["x"]
    dy = hip["y"] - shoulder["y"]
    if dy == 0:
        return 0.0
    return float(abs(np.degrees(np.arctan2(dx, dy))))

def compute_angles(frame_data: list[dict], shooting_side: str = "right") -> list[dict]:

    for frame in frame_data:
        lm = frame["landmarks"]
        s  = shooting_side

        shoulder = lm[f"{s}_shoulder"]
        elbow    = lm[f"{s}_elbow"]
        wrist    = lm[f"{s}_wrist"]
        hip      = lm[f"{s}_hip"]
        knee     = lm[f"{s}_knee"]
        ankle    = lm[f"{s}_ankle"]
        pinky = lm[f"{s}_pinky"]


        angles = {}

        if all(visible(j) for j in [shoulder, elbow, wrist]):
            angles["elbow"] = compute_angle(
                lm_to_point(shoulder),
                lm_to_point(elbow),
                lm_to_point(wrist)
            )

        if all(visible(j) for j in [hip, knee, ankle]):
            angles["knee"] = compute_angle(
                lm_to_point(hip),
                lm_to_point(knee),
                lm_to_point(ankle)
            )
        
        if all(visible(j) for j in [elbow, wrist, pinky]):
            angles["wrist"] = compute_angle(
                lm_to_point(elbow),
                lm_to_point(wrist),
                lm_to_point(pinky)
            )

        if visible(shoulder) and visible(hip):
            angles["trunk_lean"] = compute_trunk_lean(shoulder, hip)

        frame["angles"] = angles

    return frame_data