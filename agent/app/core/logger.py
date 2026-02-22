from app import config
from app.collector.system_collector import collect_system_metrics
from app.collector.process_collector import collect_suspicious_processes
from app.collector.network_collector import collect_network_usage
from app.utils.device import get_device_identity
import psutil
import datetime
import os
from PIL import ImageGrab

def detect_usb_devices():
    usb_count = 0
    for partition in psutil.disk_partitions():
        if 'removable' in partition.opts.lower():
            usb_count += 1
    return usb_count


def capture_screenshot_flag():
    try:
        # We DO NOT send image
        # Just confirm screenshot capability
        img = ImageGrab.grab()
        return True
    except:
        return False


def detect_recent_file_access():
    # DEMO VERSION
    # Just detect recently modified files in Documents
    accessed_files = 0
    documents_path = os.path.expanduser("~/Documents")

    if os.path.exists(documents_path):
        for file in os.listdir(documents_path):
            accessed_files += 1
            break  # only count 1 for demo

    return accessed_files


def build_log_payload(device_id, employee_id, employee_role):

    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    net_io = psutil.net_io_counters()

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
            "bytes_sent": net_io.bytes_sent,
            "bytes_received": net_io.bytes_recv
        },

        "external_devices": {
            "usb_connected_count": detect_usb_devices()
        },

        "screen_activity": {
            "screenshot_taken": capture_screenshot_flag()
        },

        "file_activity": {
            "recent_file_access_count": detect_recent_file_access()
        }
    }

    return payload