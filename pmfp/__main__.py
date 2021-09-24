import argparse
import threading
import sys
import time
from datetime import datetime
from pmfp import __version__

import schedule


def job():
    print("Start Job at : " + str(datetime.now()))
    print("Do something")
    print("End Job at   : " + str(datetime.now()))


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


class CliOptions:
    def __init__(self, ask_version: bool, ask_help: bool):
        self.ask_version: bool = ask_version
        self.ask_help: bool = ask_help


def _parse_args():
    parser = argparse.ArgumentParser(prog='pmfp')
    # version
    parser.add_argument(
        "-v",
        "--version",
        dest="ask_version",
        help="Show version and exit",
        action="store_true",
    )
    # config file path
    # log path?
    args = parser.parse_args()
    return CliOptions(args.ask_version, True)


def main():
    cli_options = _parse_args()
    if cli_options.ask_version:
        print(f"pmfp version {__version__}")
        sys.exit(0)

    schedule.every().minute.at(":35").do(run_threaded, job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
