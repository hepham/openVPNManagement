#!/usr/bin/env python3
import os
import re
import subprocess
import shutil
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

# Configuration paths (update as needed)
SERVER_CONF = "/etc/openvpn/server/server.conf"
CLIENT_COMMON = "/etc/openvpn/server/client-common.txt"
EASYRSA_DIR = "/etc/openvpn/server/easy-rsa"
CA_CERT = os.path.join(EASYRSA_DIR, "pki", "ca.crt")
ISSUED_DIR = os.path.join(EASYRSA_DIR, "pki", "issued")
PRIVATE_DIR = os.path.join(EASYRSA_DIR, "pki", "private")
TC_KEY = "/etc/openvpn/server/tc.key"  # TLS-crypt key file
CLIENT_DIR = os.path.expanduser("~/client")  # Final location for generated .ovpn files

def generate_client_config(client):
    """
    Create an OpenVPN configuration file (.ovpn) for the given client.
    The file includes the common configuration and inline <ca>, <cert>,
    <key>, and <tls-crypt> blocks.
    """
    ovpn_string = []
    
    # Include the common configuration file (client-common.txt)
    if os.path.exists(CLIENT_COMMON):
        with open(CLIENT_COMMON, "r") as f:
            ovpn_string.append(f.read())
    else:
        raise Exception(f"Common configuration file {CLIENT_COMMON} not found.")

    # Append additional client-specific options
    ovpn_string.append("reneg-sec 0")
    ovpn_string.append("tls-client")

    # Insert the CA certificate
    ovpn_string.append("<ca>")
    with open(CA_CERT, "r") as f:
        ovpn_string.append(f.read())
    ovpn_string.append("</ca>")

    # Insert the client certificate (strip everything before the BEGIN line)
    cert_file = os.path.join(ISSUED_DIR, f"{client}.crt")
    ovpn_string.append("<cert>")
    with open(cert_file, "r") as f:
        cert_content = f.read()
        start = cert_content.find("-----BEGIN CERTIFICATE-----")
        ovpn_string.append(cert_content[start:] if start != -1 else cert_content)
    ovpn_string.append("</cert>")

    # Insert the client private key
    key_file = os.path.join(PRIVATE_DIR, f"{client}.key")
    ovpn_string.append("<key>")
    with open(key_file, "r") as f:
        ovpn_string.append(f.read())
    ovpn_string.append("</key>")

    # Insert the tls-crypt key block (strip header if needed)
    ovpn_string.append("<tls-crypt>")
    with open(TC_KEY, "r") as f:
        tc_content = f.read()
        start = tc_content.find("-----BEGIN OpenVPN Static key")
        ovpn_string.append(tc_content[start:] if start != -1 else tc_content)
    ovpn_string.append("</tls-crypt>")

    return "\n".join(ovpn_string)


@app.route("/create_client", methods=["POST"])
def create_client():
    # Ensure that OpenVPN is installed by checking the server config file
    if not os.path.exists(SERVER_CONF):
        return jsonify({"error": "OpenVPN is not installed. Please install it first."}), 500

    # Validate input: expect JSON with a "client_name" field
    data = request.get_json()
    if not data or "client_name" not in data:
        return jsonify({"error": "Missing 'client_name' in request data."}), 400

    # Sanitize client name: allow only alphanumeric, underscore, and hyphen
    client = re.sub(r'[^0-9a-zA-Z_-]', '_', data["client_name"])

    # Check if a certificate for this client already exists
    cert_path = os.path.join(ISSUED_DIR, f"{client}.crt")
    if os.path.exists(cert_path):
        try:
            ovpn_temp = generate_client_config(client)
            return jsonify({"config":ovpn_temp}),200
        except Exception as e:
            return jsonify({"error": f"Error generating OpenVPN config: {str(e)}"}), 500

    # Create the client certificate using EasyRSA
    try:
        os.chdir(EASYRSA_DIR)
        subprocess.run(
            ["./easyrsa", "--batch", "--days=3650", "build-client-full", client, "nopass"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Error creating client certificate: {str(e)}"}), 500

    # Generate the .ovpn file
    try:
        ovpn_temp = generate_client_config(client)
    except Exception as e:
        return jsonify({"error": f"Error generating OpenVPN config: {str(e)}"}), 500


    # Return the .ovpn file as a downloadable attachment
    return jsonify({"config":ovpn_temp}),200
@app.route("/delete_client", methods=["POST"])
def delete_client():
    client_name = request.json.get("client_name")
    if not client_name:
        return jsonify({"error": "Missing client_name"}), 400
    subprocess.run([f"{EASYRSA_DIR}/easyrsa", "revoke", client_name], cwd=EASYRSA_DIR)
    subprocess.run(["systemctl", "restart", "openvpn-server@server"])
    return jsonify({"message": f"Client {client_name} deleted"})

@app.route("/monitor_clients", methods=["GET"])
def monitor_clients():
    try:
        with open(STATUS_LOG, "r") as log:
            data = log.readlines()

        clients = []
        parsing = False
        for line in data:
            if "Common Name,Real Address,Bytes Received,Bytes Sent,Connected Since" in line:
                parsing = True
                continue
            if parsing and line.strip():
                parts = line.split(",")
                clients.append({
                    "common_name": parts[0],
                    "real_address": parts[1],
                    "bytes_received": parts[2],
                    "bytes_sent": parts[3],
                    "connected_since": parts[4].strip()
                })

        return jsonify({"clients": clients})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/openvpn_monitor")
def openvpn_monitor():
    return redirect("http://your-openvpn-monitor-url")
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
