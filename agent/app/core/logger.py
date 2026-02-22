from app import config
from app.collector.system_collector import collect_system_metrics
from app.collector.process_collector import collect_suspicious_processes
from app.collector.network_collector import collect_network_usage
from app.utils.device import get_device_identity
import psutil
import datetime



def build_log_payload(device_id, employee_id, employee_role):

    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent

    payload = {
        "device_id": device_id,
        "employee_id": employee_id,
        "employee_role": employee_role,
        "device_info": {},
        "system_metrics": {
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "timestamp": datetime.datetime.utcnow().isoformat()
        },
        "network": {
            "bytes_sent": psutil.net_io_counters().bytes_sent,
            "bytes_received": psutil.net_io_counters().bytes_recv
        },
        "suspicious_processes": []
    }

    return payload