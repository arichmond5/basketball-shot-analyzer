import os
from datetime import datetime, timezone, timedelta
import json
import shutil

def cleanup_expired_jobs():
    print("Running cleanup...")
    now = datetime.now(timezone.utc)
    storage_path = "storage"
    #open storage path and pull all job_ids
    for job_id in os.listdir(storage_path):
        print(f"checking {job_id}")
        #go in each job_id, get results.json, look for expires_at, if datetime.now(timezone.utc) > expires_at, delete folder
        job_path = os.path.join(storage_path, job_id)
        result_file = os.path.join(job_path, "result.json")

        if not os.path.exists(result_file):
            continue

        with open(result_file, "r") as f:
            result = json.load(f)
        
        expires_at = datetime.fromisoformat(result["expires_at"].replace("Z", "+00:00"))
        if now > expires_at:
            shutil.rmtree(f"storage/{job_id}")

    print("Cleanup complete")
