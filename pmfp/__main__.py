import argparse
import logging
import threading
import sys
import time
from datetime import datetime

import json_log_formatter

from pmfp import __version__

import schedule


def job():
    logger = logging.getLogger(__name__)
    logger.info("Start Job at : " + str(datetime.now()))
    logger.info("Do something")
    logger.info("End Job at   : " + str(datetime.now()))


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


class CliOptions:
    def __init__(self, ask_version: bool, ask_help: bool, json_logging_path: str):
        self.ask_version: bool = ask_version
        self.ask_help: bool = ask_help
        self.json_logging_path = json_logging_path

    def is_logging_activated(self):
        return self.json_logging_path is not None


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
    parser.add_argument(
        "-j",
        "--json-logging-path",
        dest="json_logging_path",
        help="Activate JSON Logging on this file",
        type=str,
    )
    # TODO: config file path
    args = parser.parse_args()
    return CliOptions(ask_version=args.ask_version,
                      ask_help=True,
                      json_logging_path=args.json_logging_path)


def set_json_logging(file_path: str):
    print(f"Logging sent to {file_path}")
    formatter = json_log_formatter.JSONFormatter()

    logging.StreamHandler()
    json_handler = logging.FileHandler(filename=file_path)
    json_handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(json_handler)
    logger.setLevel(logging.INFO)


def set_stdout_logging():
    print(f"Logging sent to sdtout")

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logging.StreamHandler()
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setFormatter(formatter)

    logger = logging.getLogger(__name__)
    logger.addHandler(stdout_handler)
    logger.setLevel(logging.DEBUG)
    logger.debug("Logging in DEBUG level")


def main():

    cli_options = _parse_args()
    if cli_options.ask_version:
        print(f"pmfp version {__version__}")
        sys.exit(0)

    if cli_options.is_logging_activated():
        set_json_logging(cli_options.json_logging_path)
    else:
        set_stdout_logging()

    schedule.every().minute.at(":35").do(run_threaded, job)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
