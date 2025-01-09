#!/usr/bin/python3
from schedule import repeat, every, run_pending

import timelapse

cfg: object = timelapse.loadConfig()
start_time: str = cfg["variable"]["start_time"]
debug: bool = cfg["debug"]


@repeat(every().day.at(start_time))
def run() -> None:
    """
    take series of photos for timelapse
    at a prescheduled time
    """
    timestamp: str = timelapse.getTimestamp()
    timelapse.sendTimelapse(cfg, timestamp)


def main() -> None:
    while True:
        run_pending()


if __name__ == "__main__":
    if debug:
        run()
    else:
        main()
