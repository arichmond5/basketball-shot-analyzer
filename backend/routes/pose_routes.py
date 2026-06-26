from fastapi import APIRouter, UploadFile, File
import os
import uuid
import shutil

from analysis.pose_analysis import analyze_video

router = APIRouter()

VIDEOS_DIR = "videos"
os.makedirs(VIDEOS_DIR, exist_ok=True)


@router.post("/upload-and-analyze")
async def upload_and_analyze(file: UploadFile = File(...)):

    # 1. Save uploaded file
    file_id   = str(uuid.uuid4())
    file_path = os.path.join(VIDEOS_DIR, f"{file_id}.mp4")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Hand off to analysis pipeline
    result = analyze_video(file_id, file_path)

    return result