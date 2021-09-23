import threading
import time
from datetime import datetime

import schedule


def job():
    print("Start Job at : " + str(datetime.now()))
    print("Do something")
    print("End Job at   : " + str(datetime.now()))


def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


def main():
    schedule.every().minute.at(":35").do(run_threaded, job)
    while True:
        schedule.run_pending()
        time.sleep(1)
