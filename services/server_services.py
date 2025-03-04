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

        url = "{ipServer}/create_client/wg0"
        payload = json.dumps({
        "name": f"{username}"
        })
        
        response = session.request("POST", url,headers={'Content-Type': 'application/json'},data=payload)
        if (response.status_code == 200):
            return response.text

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


def get_wg(ipServer, username):
    url = f"http://{ipServer}:51821/api/wireguard/client"

    headers = {
        'Cookie': 'connect.sid=s%3AHhzpWlSMeWXduBfBjzyflOTeOLxUjQQM.7ME8c5A%2BvdHIKNXM%2B2wl9%2Fhpk00hEBjb6th1nkSdYwg',
        'Content-Type': 'application/json'
    }

    payload = json.dumps({
        "name": username
    })
    response = requests.request("GET", url, headers=headers)
    check=False
    if(response.status_code == 200):
        data = json.loads(response.text)
        for client in data:
            if(client["name"] == username):
                check=True
                break
    if(check==False):
        requests.request("POST", url, headers=headers, data=payload)

    response = requests.request("GET", url, headers=headers)
    if (response.status_code == 200):
        data = json.loads(response.text)
        for client in data:
            if (client["name"] == username):
                url = f"http://{ipServer}:51821/api/wireguard/client/{client['id']}/configuration"
                response = requests.request("GET", url, headers=headers)
                print(response.text)
                return response.text

    return "error"
