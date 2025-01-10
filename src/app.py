#!/usr/bin/python3
import json

from flask import Flask, render_template, request
from flask_apscheduler import APScheduler

import timelapse

app = Flask(__name__)

with open("config.json", "r") as f:
    cfg = json.load(f)
    context = dict(cfg["variable"])


class Config:
    SCHEDULER_API_ENABLED = True


app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


def job():
    """Job to be run at scheduled time"""
    timestamp = timelapse.getTimestamp()
    timelapse.sendTimelapse(cfg, timestamp)


def updateScheduledJob(id: str) -> None:
    """Change the starting time of script from the server input"""
    scheduler.remove_job(id=id)
    time_parts = context["start_time"].split(":")
    hour, mins = time_parts[0], time_parts[1]
    scheduler.add_job("id", func=job, trigger="cron", hour=hour, minute=mins)
    print(f"Job restarted with start time of {hour}:{mins}")


start_hour = context["start_time"].split(":")[0]
start_mins = context["start_time"].split(":")[1]

scheduler.add_job("job", func=job, trigger="cron", hour=start_hour, minute=start_mins)


@app.route("/")
def view_form():
    print(f"cfg: {cfg['variable']}")
    print(f"context: {context}")
    print("job started")
    return render_template("index.html", context=context)


@app.route("/handle_request", methods=["GET", "POST"])
def handle_request():
    if request.method == "POST":
        for key in context:
            if request.form[key]:
                context[key] = request.form[key]

    if request.method == "GET":
        for key in context:
            if request.args.get(key):
                context[key] = request.args.get(key)

    cfg["variable"] = context

    updateScheduledJob(id="job")

    return render_template("index.html", context=context)


if __name__ == "__main__":
    app.run(debug=True)
