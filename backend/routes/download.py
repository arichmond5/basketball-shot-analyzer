from fastapi import APIRouter
from fastapi.responses import FileResponse
import zipfile
import os
import tempfile
import json

router = APIRouter()

@router.get("/download/{job_id}")
def create_zip(job_id: str):
    job_path = os.path.join("storage", job_id)

    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
        zip_path = tmp.name

    with zipfile.ZipFile(zip_path, "w") as zipf:

        # Overlay video
        overlay_path = os.path.join(job_path, "overlay", "overlay.mp4")
        zipf.write(
            overlay_path,
            arcname="overlay.mp4"
        )

        # Snapshots
        snapshots_path = os.path.join(job_path, "snapshots")

        for filename in os.listdir(snapshots_path):
            file_path = os.path.join(snapshots_path, filename)

            zipf.write(
                file_path,
                arcname=f"snapshots/{filename}"
            )

        # Feedback from result.json
        result_path = os.path.join(job_path, "result.json")

        with open(result_path, "r") as f:
            result = json.load(f)

        feedback = result["feedback"]

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False
        ) as feedback_file:
            json.dump(feedback, feedback_file, indent=4)
            feedback_path = feedback_file.name

        zipf.write(
            feedback_path,
            arcname="feedback.json"
        )

    return FileResponse(
        zip_path,
        filename="shot-analysis.zip",
        media_type="application/zip"
    )
