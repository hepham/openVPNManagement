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
    url=f"{ipServer}/create_client"
    payload = json.dumps({
    "client_name": username
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if(response.status_code==200):
        data=json.loads(response.text)
        # print(data)
        config = data["config"]
        return config
    return "error"