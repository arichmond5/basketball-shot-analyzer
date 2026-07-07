from cleanup import cleanup_expired_jobs
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

scheduler.add_job(
    cleanup_expired_jobs,
    "interval",
    minutes=1
)

scheduler.start()
