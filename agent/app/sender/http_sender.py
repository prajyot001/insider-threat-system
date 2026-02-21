import requests

def send_log(server_url, data):
    try:
        response = requests.post(server_url, json=data, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False