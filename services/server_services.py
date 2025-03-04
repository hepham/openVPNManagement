import requests
import json


def createClient(ipServer, username):
    url = f"{ipServer}/add_user"

    payload = json.dumps({
        "username": username
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)


def get_wireguard(ipServer, username):
    
    url = f"{ipServer}/auth"

    payload = {'password': 'admin',
    'username': 'admin'}

    session = requests.Session()  # Tạo session để duy trì cookie
    response = session.post(url, data=payload)
    print(session.cookies.get_dict())

    if response.status_code == 200:

        url = f"{ipServer}/create_client/wg0"
        payload = json.dumps({
        "name": f"{username}"
        })
        
        response = session.request("POST", url,headers={'Content-Type': 'application/json'},data=payload)
        if (response.status_code == 200):
            return response.text
    return "error"

def get_meta_data(ip):
    metadata = {}
    url = f"https://ipinfo.io/{ip}/json"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if (response.status_code == 200):
        data = json.loads(response.text)
        metadata["region"] = data["region"]
        metadata["postal"] = data["postal"]
        loc = data["loc"]
        values = loc.split(",")
        metadata["latitude"] = values[0]
        metadata["longitude"] = values[1]
        return metadata
    return "error"

