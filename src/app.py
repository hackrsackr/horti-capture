#!/usr/bin/python3
import json

from schedule import repeat, every, run_pending
from flask import Flask, render_template, request

import timelapse


app = Flask(__name__)

with open("config.json", "r") as f:
    cfg = json.load(f)
    context = dict(cfg["variable"])


@repeat(every().day.at(context["start_time"]))
def run():
    timestamp = timelapse.getTimestamp()
    timelapse.sendTimelapse(cfg, timestamp)


@app.route("/")
def view_form():
    print(f"cfg: {cfg['variable']}")
    print(f"context: {context}")
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

    print(f"cfg: {cfg['variable']}")
    print(f"context: {context}")

    return render_template("index.html", context=context)


if __name__ == "__main__":
    app.run(debug=True)
