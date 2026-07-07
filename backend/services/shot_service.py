"""
Background worker that runs pipeline + saves results.
"""

import os
import json

from services.shot_pipeline import run_shot_pipeline


def analyze_shot(job_id: str, file_path: str, snapshot_dir: str, overlay_dir: str):
    # 1. run pure pipeline
    result = run_shot_pipeline(
        file_path=file_path,
        job_id=job_id,
        snapshot_dir=snapshot_dir,
        overlay_dir=overlay_dir,
    )

    # 2. persist result
    result_path = os.path.join("storage", job_id, "result.json")

    with open(result_path, "w") as f:
        json.dump(result, f)

    return result