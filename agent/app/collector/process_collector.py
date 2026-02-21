import psutil

SUSPICIOUS_KEYWORDS = ["cmd", "powershell", "nmap", "wireshark"]

def collect_suspicious_processes():
    suspicious = []

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info["name"]
            for keyword in SUSPICIOUS_KEYWORDS:
                if keyword.lower() in name.lower():
                    suspicious.append({
                        "process_name": name,
                        "pid": proc.info["pid"]
                    })
                    break
        except:
            pass

    return suspicious