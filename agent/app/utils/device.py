import socket
import uuid
import platform

def get_device_identity():
    return {
        "hostname": socket.gethostname(),
        "mac_address": ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                                 for ele in range(0, 8*6, 8)][::-1]),
        "os": platform.system(),
        "architecture": platform.machine()
    }