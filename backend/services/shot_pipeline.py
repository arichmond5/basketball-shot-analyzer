"""
Runs the complete basketball shot analysis pipeline.

Pipeline:
1. Extract pose data
2. Detect shooting side
3. Compute joint angles
4. Segment shot phases
5. Select keyframes
6. Generate feedback
7. Create overlay video and snapshots
"""

from processing.extract_landmarks import analyze_video
from analysis.detect_side import detect_shooting_side
from analysis.compute_angles import compute_angles
from analysis.shot_segmenter import shot_segmenter
from feedback.snapshot_feedback import generate_snapshot_feedback
from processing.create_overlays import create_overlay_video_and_snapshots
from processing.keyframe_selector import get_keyframe_data

from datetime import datetime, timedelta, timezone


def run_shot_pipeline(
    job_id: str,
    file_path: str,
    snapshot_dir: str,
    overlay_dir: str
):
    # 1. Extract pose data
    frame_data = analyze_video(file_path)

    # 2. Detect shooting side
    shooting_side = detect_shooting_side(frame_data)

    # 3. Compute joint angles
    frame_data = compute_angles(frame_data, shooting_side)

    # 4. Segment shot phases
    phases = shot_segmenter(frame_data)

    # 5. Select keyframes
    keyframe_data = get_keyframe_data(frame_data, phases, shooting_side)

    # 6. Generate feedback
    feedback = generate_snapshot_feedback(keyframe_data)

    # 7. Create overlay video and snapshots
    overlay_url, snapshot_urls = create_overlay_video_and_snapshots(
        file_path=file_path,
        job_id=job_id,
        phases=phases,
        frame_data=frame_data,
        shooting_side=shooting_side,
        snapshot_dir=snapshot_dir,
        overlay_dir=overlay_dir
    )

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=30) #30 minute expiration time

    return {
        "status": "done",
        "feedback": feedback,
        "snapshots": snapshot_urls,
        "overlay_url": overlay_url,
        "timestamp": now.isoformat(),
        "expires_at": expires_at.isoformat() #allows json to format
    }
