from flask import Flask
from flask_apscheduler import APScheduler

app = Flask(__name__)


# Configure scheduler
class Config:
    SCHEDULER_API_ENABLED = True


app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

time_stamp = "18:28"
time_parts = time_stamp.split(":")
hour = time_parts[0]
minutes = time_parts[1]


# Define a scheduled job
# @scheduler.task("cron", id="do_job1", hour=hour, minute=minutes)
def job1():
    print("This job runs every 30 seconds")


scheduler.add_job("job", func=job1, trigger="cron", hour=hour, minute=minutes)
print("job started")
print(hour)
print(minutes)


hour = 18
minutes = 33

scheduler.remove_job("job")
print("job removed")
scheduler.add_job("job", func=job1, trigger="cron", hour=hour, minute=minutes)
print("job restarted")
print(hour)
print(minutes)

if __name__ == "__main__":
    app.run(debug=True)
