from app.core.scheduler import run_scheduler
from app.core.logger import build_log_payload
from app.sender.http_sender import send_log
from app.config import load_config


def main():
    config = load_config()

    def job():
        payload = build_log_payload(
            device_id=config["device_id"],
            employee_id=config["employee_id"],
            employee_role=config["employee_role"]
        )

        success = send_log(config["server_url"], payload)
        print(config["server_url"])
        

        if success:
            print("Log sent successfully")
        else:
            print("Failed to send log")

    print("Monitoring Agent Started...")
    run_scheduler(config["log_interval_seconds"], job)


if __name__ == "__main__":
    main()