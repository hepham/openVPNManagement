import re

def get_user_and_server_id(input_string):
    pattern = r'^user:(\w+)\s+server_id:(\w+)$'
    match = re.match(pattern, input_string)
    if match:
        user = match.group(1) 
        server_id = match.group(2)  
        return {"user": user, "server_id": server_id}
    else:
        return {"error": "Invalid format"}

def check_format(input_string):
    pattern = r'^user:\w+\s+server_id:\w+$'
    
    if re.match(pattern, input_string):
        return True
    return False
def get_certificate(certificate_string):
    pattern = r"-----BEGIN CERTIFICATE-----\s*(.*?)\s*-----END CERTIFICATE-----"

    match = re.search(pattern, certificate_string, re.DOTALL)

    if match:
        certificate_content = match.group(1)  
        return certificate_content
    else:
        print("Certificate not found.")
