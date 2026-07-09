"""
Background worker that runs pipeline + saves results.
"""

import os
import json
import traceback

from services.shot_pipeline import run_shot_pipeline


def analyze_shot(job_id: str, file_path: str, snapshot_dir: str, overlay_dir: str):
    try:
        print(f"Starting analysis for job {job_id}")

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

        print(f"Analysis complete for job {job_id}")

        return result

    except Exception as e:
        print(f"ANALYSIS FAILED for job {job_id}: {e}")
        traceback.print_exc()
        raise
