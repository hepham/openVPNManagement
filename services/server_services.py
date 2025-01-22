import requests
import json
def createClient(ipServer,username):
    url = f"{ipServer}/add_user"

    payload = json.dumps({
    "username": username
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
def get_ovpn(ipServer,username):
    url = f"{ipServer}/get_ovpn/{username}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        temp_file = f"./ovpn/{username}.ovpn"
    with open(temp_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)
        return temp_file

    return "error"

