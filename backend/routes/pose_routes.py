from fastapi import APIRouter, UploadFile, File
from fastapi.staticfiles import StaticFiles
import os
import uuid
import shutil

from processing.shot_analysis import analyze_shot

router = APIRouter()

VIDEOS_DIR   = "videos"
SNAPSHOT_DIR = "snapshots"
os.makedirs(VIDEOS_DIR,   exist_ok=True)
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

@router.post("/upload-and-analyze")
async def upload_and_analyze(file: UploadFile = File(...)):
    file_id   = str(uuid.uuid4())
    file_path = os.path.join(VIDEOS_DIR, f"{file_id}.mp4")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_shot(file_id, file_path)

    return result