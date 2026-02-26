from typing import List
from .config import MAX_IN_MEMORY_LOGS

logs_storage: List[dict] = []


def add_log(log: dict):
    logs_storage.append(log)

    # Prevent unlimited memory growth
    if len(logs_storage) > MAX_IN_MEMORY_LOGS:
        logs_storage.pop(0)


def get_logs():
    return logs_storage


def clear_logs():
    logs_storage.clear()