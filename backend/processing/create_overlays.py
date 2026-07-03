import cv2
import os

SNAPSHOT_DIR = "snapshots"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

CONNECTIONS = [
    ("right_shoulder", "left_shoulder"),
    ("right_shoulder", "right_hip"),
    ("left_shoulder", "left_hip"),
    ("right_hip", "left_hip"),
    ("right_hip", "right_knee"),
    ("right_knee", "right_ankle"),
    ("left_hip", "left_knee"),
    ("left_knee", "left_ankle"),
]

LM = {
    "left_shoulder":  11, "right_shoulder": 12,
    "left_elbow":     13, "right_elbow":    14,
    "left_wrist":     15, "right_wrist":    16,
    "left_pinky":     17, "right_pinky":    18,
    "left_hip":       23, "right_hip":      24,
    "left_knee":      25, "right_knee":     26,
    "left_ankle":     27, "right_ankle":    28,
}

def pick_snapshot_frame(phase_frames: list[dict], phase: str, shooting_side) -> dict:
    """Pick the most representative frame for each phase."""
    if phase == "LOADING":
        return min(phase_frames, key=lambda f: f["angles"].get("knee", 180))
    elif phase == "SET_POINT":
        return min(phase_frames, key=lambda f: f["angles"].get("elbow", 180))
    elif phase == "RELEASE":
        return max(
            [
                f for f in phase_frames
                if f["landmarks"][f"{shooting_side}_elbow"]["y"]
                < f["landmarks"][f"{shooting_side}_shoulder"]["y"]
            ],
            key=lambda f: f["angles"].get("elbow", 0)
        )
    return phase_frames[0]

def draw_overlay(frame, landmarks: dict, shooting_side: str, w: int, h: int):
    connections = CONNECTIONS + [
        (f"{shooting_side}_shoulder", f"{shooting_side}_elbow"),
        (f"{shooting_side}_elbow", f"{shooting_side}_wrist"),
    ]
    allowed = {
        f"{shooting_side}_shoulder",
        f"{shooting_side}_elbow",
        f"{shooting_side}_wrist",
        f"{shooting_side}_pinky",
        "left_shoulder",
        "right_shoulder",
        "left_hip",
        "right_hip",
        "left_knee",
        "right_knee",
        "left_ankle",
        "right_ankle",
    }

    for a, b in connections:
        if a not in landmarks or b not in landmarks:
            continue
        if landmarks[a]["visibility"] < 0.75 or landmarks[b]["visibility"] < 0.75:
            continue

        pa = (int(landmarks[a]["x"] * w), int(landmarks[a]["y"] * h))
        pb = (int(landmarks[b]["x"] * w), int(landmarks[b]["y"] * h))
        cv2.line(frame, pa, pb, (200, 200, 200), 2, cv2.LINE_AA)

    for name, lm in landmarks.items():
        if name not in allowed:
            continue

        if lm["visibility"] < 0.75:
            continue

        px = int(lm["x"] * w)
        py = int(lm["y"] * h)

        cv2.circle(frame, (px, py), 5, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.circle(frame, (px, py), 5, (0, 150, 255), 1, cv2.LINE_AA)

def draw_angles(frame, landmarks: dict, angles: dict, shooting_side: str, w: int, h: int):
    s = shooting_side

    def pt(name):
        lm = landmarks.get(name)
        if lm is None:
            return None
        return (int(lm["x"] * w), int(lm["y"] * h))

    if "elbow" in angles:
        shoulder = pt(f"{s}_shoulder")
        elbow    = pt(f"{s}_elbow")
        wrist    = pt(f"{s}_wrist")
        if all([shoulder, elbow, wrist]):
            cv2.line(frame, shoulder, elbow, (0, 255, 200), 2)
            cv2.line(frame, elbow,    wrist, (0, 255, 200), 2)
            cv2.putText(frame, f"Elbow: {angles['elbow']:.0f}", elbow,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 200), 2)

    if "knee" in angles:
        hip   = pt(f"{s}_hip")
        knee  = pt(f"{s}_knee")
        ankle = pt(f"{s}_ankle")
        if all([hip, knee, ankle]):
            cv2.line(frame, hip,   knee,  (255, 180, 0), 2)
            cv2.line(frame, knee,  ankle, (255, 180, 0), 2)
            cv2.putText(frame, f"Knee: {angles['knee']:.0f}", knee,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 180, 0), 2)
    
    if "trunk_lean" in angles:
        shoulder = pt(f"{s}_shoulder")
        hip      = pt(f"{s}_hip")
        if all([shoulder, hip]):
            cv2.line(frame, shoulder, hip, (255, 0, 255), 2)
            # draw a vertical reference line from hip straight up
            vertical_top = (hip[0], hip[1] - 100)
            cv2.line(frame, hip, vertical_top, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Lean: {angles['trunk_lean']:.0f}", 
                        (shoulder[0] + 10, shoulder[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

def create_overlay_video_and_snapshots(
    file_path: str,
    file_id: str,
    phases: dict,
    data_frame: list[dict],
    shooting_side: str
) -> tuple[str, dict[str, str]]:

    frame_lookup = {f["frame_index"]: f for f in data_frame}

    cap = cv2.VideoCapture(file_path)
    w   = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h   = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    OVERLAY_DIR = "overlays"
    os.makedirs(OVERLAY_DIR, exist_ok=True)

    out_path = os.path.join(OVERLAY_DIR, f"{file_id}_overlay.mp4")
    writer = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"avc1"), fps, (w, h))

    # figure out which frame index we want for each phase snapshot ahead of time
    snapshot_targets = {}
    for phase, (start, end) in phases.items():
        phase_frames = [
            frame_lookup[i]
            for i in range(start, end + 1)
            if i in frame_lookup
        ]
        if phase_frames:
            snapshot_targets[phase] = pick_snapshot_frame(phase_frames, phase, shooting_side)["frame_index"]

    snapshot_paths = {}
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx in frame_lookup:
            f = frame_lookup[frame_idx]
            draw_overlay(frame, f["landmarks"], shooting_side, w, h)
            draw_angles(frame, f["landmarks"], f.get("angles", {}), shooting_side, w, h)

            # if this is a snapshot target frame, save it before writing
            for phase, target_idx in snapshot_targets.items():
                if frame_idx == target_idx:
                    snap_path = os.path.join(SNAPSHOT_DIR, f"{file_id}_{phase}.jpg")
                    cv2.imwrite(snap_path, frame)
                    snapshot_paths[phase] = f"http://localhost:8000/snapshots/{file_id}_{phase}.jpg"

        writer.write(frame)
        frame_idx += 1

    cap.release()
    writer.release()

    overlay_url = f"http://localhost:8000/overlays/{file_id}_overlay.mp4"
    return overlay_url, snapshot_paths
