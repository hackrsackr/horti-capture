from flask_apscheduler import APScheduler


def job():
    print("doing job")


class Config:
    SCHEDULER_API_ENABLED = True


def updateStartTime(time: str):
    time_parts = time.split(":")
    hour = time_parts[0]
    mins = time_parts[1]
    print(f"New start time is {hour}:{mins}")

    return hour, mins


def updateScheduledJob(id: str, hr, min):
    APScheduler.remove_job(id=id)
    print("job removed")
    APScheduler.add_job("id", func=job, trigger="cron", hour=hr, minute=min)
    print(f"Job restarted with start time of {hr}:{min}")
