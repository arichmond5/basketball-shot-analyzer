from .extract_landmarks import analyze_video
from analysis.detect_side import detect_shooting_side
from analysis.compute_angles import compute_angles
from analysis.shot_segmenter import shot_segmenter
from feedback.snapshot_feedback import generate_snapshot_feedback
from processing.create_overlays import create_overlay_video_and_snapshots
from processing.keyframe_selector import get_keyframe_data

def analyze_shot(file_id: str, file_path: str):
    frame_data = analyze_video(file_path)
    shooting_side = detect_shooting_side(frame_data)
    frame_data = compute_angles(frame_data, shooting_side)
    phases = shot_segmenter(frame_data)
    keyframe_data = get_keyframe_data(frame_data, phases, shooting_side)
    feedback = generate_snapshot_feedback(keyframe_data)
    overlay_url, snapshots = create_overlay_video_and_snapshots(
        file_path, file_id, phases, frame_data, shooting_side
    )

    return {"feedback": feedback, "snapshots": snapshots, "overlay_url": overlay_url}

