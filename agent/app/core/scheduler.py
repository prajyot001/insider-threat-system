import time

def run_scheduler(interval, task):
    while True:
        task()
        time.sleep(interval)