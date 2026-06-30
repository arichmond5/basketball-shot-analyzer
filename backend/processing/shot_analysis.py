from .extract_landmarks import analyze_video
from analysis.detect_side import detect_shooting_side
from analysis.compute_angles import compute_angles
from analysis.shot_segmenter import shot_segmenter
from metrics.shot_metrics import compute_shot_metrics
from metrics.feedback import generate_feedback
from processing.create_overlays import create_overlay_video_and_snapshots

def analyze_shot(file_id: str, file_path: str):
    data_frame = analyze_video(file_id, file_path)
    shooting_side = detect_shooting_side(data_frame)
    data_frame = compute_angles(data_frame, shooting_side)
    phases = shot_segmenter(data_frame)
    metrics = compute_shot_metrics(data_frame, phases)
    feedback = generate_feedback(metrics)
    overlay_url, snapshots = create_overlay_video_and_snapshots(
        file_path, file_id, phases, data_frame, shooting_side
    )

    return {"feedback": feedback, "snapshots": snapshots, "overlay_url": overlay_url}

