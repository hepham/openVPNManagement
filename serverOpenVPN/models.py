import os
import re
import subprocess
from flask import jsonify

class OpenVPNModel:
    SERVER_CONF = "/etc/openvpn/server/server.conf"
    CLIENT_COMMON = "/etc/openvpn/server/client-common.txt"
    EASYRSA_DIR = "/etc/openvpn/server/easy-rsa"
    CA_CERT = os.path.join(EASYRSA_DIR, "pki", "ca.crt")
    ISSUED_DIR = os.path.join(EASYRSA_DIR, "pki", "issued")
    PRIVATE_DIR = os.path.join(EASYRSA_DIR, "pki", "private")
    TC_KEY = "/etc/openvpn/server/tc.key"

    @staticmethod
    def generate_client_config(client):
        """Create an OpenVPN configuration file (.ovpn) for the given client."""
        ovpn_string = []

        if os.path.exists(OpenVPNModel.CLIENT_COMMON):
            with open(OpenVPNModel.CLIENT_COMMON, "r") as f:
                ovpn_string.append(f.read())
        else:
            raise Exception(f"Common configuration file {OpenVPNModel.CLIENT_COMMON} not found.")

        ovpn_string.append("reneg-sec 0")
        ovpn_string.append("tls-client")

        ovpn_string.append("<ca>")
        with open(OpenVPNModel.CA_CERT, "r") as f:
            ovpn_string.append(f.read())
        ovpn_string.append("</ca>")

        cert_file = os.path.join(OpenVPNModel.ISSUED_DIR, f"{client}.crt")
        ovpn_string.append("<cert>")
        with open(cert_file, "r") as f:
            cert_content = f.read()
            start = cert_content.find("-----BEGIN CERTIFICATE-----")
            ovpn_string.append(cert_content[start:] if start != -1 else cert_content)
        ovpn_string.append("</cert>")


        key_file = os.path.join(OpenVPNModel.PRIVATE_DIR, f"{client}.key")
        ovpn_string.append("<key>")
        with open(key_file, "r") as f:
            ovpn_string.append(f.read())
        ovpn_string.append("</key>")

        # Insert the tls-crypt key block
        ovpn_string.append("<tls-crypt>")
        with open(OpenVPNModel.TC_KEY, "r") as f:
            tc_content = f.read()
            start = tc_content.find("-----BEGIN OpenVPN Static key")
            ovpn_string.append(tc_content[start:] if start != -1 else tc_content)
        ovpn_string.append("</tls-crypt>")

        return "\n".join(ovpn_string)

    @staticmethod
    def create_client_certificate(client):
        """Create a client certificate using EasyRSA."""
        try:
            os.chdir(OpenVPNModel.EASYRSA_DIR)
            subprocess.run(
                ["./easyrsa", "--batch", "--days=3650", "build-client-full", client, "nopass"],
                check=True
            )
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error creating client certificate: {str(e)}")

    @staticmethod
    def revoke_client(client_name):
        """Revoke a client certificate using EasyRSA."""
        subprocess.run([f"{OpenVPNModel.EASYRSA_DIR}/easyrsa", "revoke", client_name], cwd=OpenVPNModel.EASYRSA_DIR)
        subprocess.run(["systemctl", "restart", "openvpn-server@server"])

    @staticmethod
    def client_exists(client):
        """Check if a client certificate exists."""
        cert_path = os.path.join(OpenVPNModel.ISSUED_DIR, f"{client}.crt")
        return os.path.exists(cert_path)
