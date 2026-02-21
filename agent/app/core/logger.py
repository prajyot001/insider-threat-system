from collector.system_collector import collect_system_metrics
from collector.process_collector import collect_suspicious_processes
from collector.network_collector import collect_network_usage
from utils.device import get_device_identity

def build_log_payload(device_id):
    return {
        "device_id": device_id,
        "device_info": get_device_identity(),
        "system_metrics": collect_system_metrics(),
        "network": collect_network_usage(),
        "suspicious_processes": collect_suspicious_processes()
    }