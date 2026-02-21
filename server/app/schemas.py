from pydantic import BaseModel
from typing import List, Dict, Any


class ProcessInfo(BaseModel):
    process_name: str
    pid: int


class DeviceInfo(BaseModel):
    hostname: str
    mac_address: str
    os: str
    architecture: str


class SystemMetrics(BaseModel):
    timestamp: str
    cpu_usage: float
    ram_usage: float
    disk_usage: float


class NetworkMetrics(BaseModel):
    bytes_sent: int
    bytes_received: int


class LogCreate(BaseModel):
    device_id: str
    device_info: DeviceInfo
    system_metrics: SystemMetrics
    network: NetworkMetrics
    suspicious_processes: List[ProcessInfo]