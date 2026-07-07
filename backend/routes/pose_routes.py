"""
Upload + async analysis pipeline for basketball shot system.

Flow:
1. Upload video → create job_id immediately
2. Return job_id to frontend (fast response)
3. Run analysis in background
4. Save result.json when done
5. Frontend polls /results/{job_id}
"""

from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
import os
import uuid
import shutil
import json

from services.shot_service import analyze_shot

router = APIRouter()

BASE_DIR = "storage"
os.makedirs(BASE_DIR, exist_ok=True)


# -----------------------------
# 1. UPLOAD ENDPOINT
# -----------------------------
@router.post("/upload-and-analyze")
async def upload_and_analyze(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    # 1. Create job id
    job_id = str(uuid.uuid4())

    # 2. Create job directories
    job_dir = os.path.join(BASE_DIR, job_id)
    video_dir = os.path.join(job_dir, "video")
    snapshot_dir = os.path.join(job_dir, "snapshots")
    overlay_dir = os.path.join(job_dir, "overlay")

    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(snapshot_dir, exist_ok=True)
    os.makedirs(overlay_dir, exist_ok=True)

    # 3. Save uploaded video
    file_path = os.path.join(video_dir, "input.mp4")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 4. run analysis in background
    background_tasks.add_task(
        analyze_shot,
        job_id,
        file_path,
        snapshot_dir,
        overlay_dir
    )

    # 5. return so user can be directed to ResultsPage/LoadingScreen
    return {
        "job_id": job_id
    }


# -----------------------------
# 2. RESULTS ENDPOINT
# -----------------------------
@router.get("/results/{job_id}")
def get_results(job_id: str):
    job_dir = os.path.join(BASE_DIR, job_id)
    result_path = os.path.join(job_dir, "result.json")

    # job_id folder does not exist (expired/deleted)
    if not os.path.exists(job_dir):
        raise HTTPException(
            status_code=404,
            detail="Session expired"
        )

    # still processing
    if not os.path.exists(result_path):
        return {
            "status": "processing"
        }

    # done
    with open(result_path, "r") as f:
        return json.load(f)
    