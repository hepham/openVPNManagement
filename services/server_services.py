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
    url = f"http://ip-api.com/json/{ip}"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    if (response.status_code == 200):
        data = json.loads(response.text)
        metadata["region"] = data["regionName"]
        metadata["postal"] = data["zip"]
        metadata["latitude"] = data["lat"]
        metadata["longitude"] = data["lon"]
        metadata["country"] =data["country"]
        metadata["city"]=data["city"]
        
        return metadata
    return "error"

