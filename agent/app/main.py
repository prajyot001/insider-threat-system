from core.scheduler import run_scheduler
from core.logger import build_log_payload
from sender.http_sender import send_log
from config import load_config

config = load_config()

def job():
    payload = build_log_payload(config["device_id"])
    success = send_log(config["server_url"], payload)

    if success:
        print("Log sent successfully")
    else:
        print("Failed to send log")

if __name__ == "__main__":
    print("Monitoring Agent Started...")
    run_scheduler(config["log_interval_seconds"], job)