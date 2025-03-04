import os
from flask import Blueprint, request, jsonify, send_file
from models import db, rsaRedis, Server
from services.server_services import createClient, get_wireguard
from services.rsa_services import generate_rsa_key_pair, encrypt, decrypt
from services.format_check import get_user_and_server_id, get_certificate
from services.aes_service import encrypt_with_aes
from urllib.parse import urlparse
from services.server_services import get_meta_data
import json
import re
server_bp = Blueprint('server_bp', __name__)


@server_bp.route('/listServer', methods=['GET'])
def get_servers():
    servers = Server.query.all()
    server_list = _build_server_list(servers)
    # print("server_list:",server_list)
    server_list_json = json.dumps(server_list)
    key = os.getenv("ENCRYPTION_KEY", "SMJUH41TkNyChU8c5kWPiA==")
    encrypted_message = encrypt_with_aes(server_list_json, key)
    # print("encrypted_message:",encrypted_message)
    return jsonify({"message": encrypted_message}), 200


def _build_server_list(servers):
    """Xây dựng danh sách server từ cơ sở dữ liệu."""
    return [
        {
            'id': server.id,
            #'IP':server.IP,
            'country': server.country,
            'city': server.city,
            'flag': server.flag,
            'isFree': server.isFree,
            'category': server.category,
            'description': server.description,
            'latitude': server.latitude,
            'longitude': server.longitude,
            'region': server.region,
            'postal': server.postal
            # "IP": server.IP
        } for server in servers
    ]





@server_bp.route('/server', methods=['POST'])
def add_server():
    data = request.json
    existing_server = Server.query.filter_by(IP=data['IP']).first()

    if existing_server:
        return jsonify({'error': 'Server with this IP already exists'}), 400
    parsed_url = urlparse(data["IP"])

    ip_address = parsed_url.hostname
    print(ip_address)
    metadata = get_meta_data(ip_address)
    if (metadata == "error"):
        return jsonify({'error': 'problem get metadata'}), 400
    new_server = Server(
        country=data['country'],
        city=data['city'],
        flag=data['flag'],
        IP=data["IP"],
        isFree=data['isFree'],
        description=data['description'],
        category=data["category"],
        latitude=metadata["latitude"],
        longitude=metadata["longitude"],
        region=metadata["region"],
        postal=metadata["postal"]
    )
    db.session.add(new_server)
    db.session.commit()
    return jsonify({'message': 'Server added successfully'}), 201


@server_bp.route('/server/list', methods=['POST'])
def add_server_list():
    data = request.json

    # Check that the input data is a list
    if not isinstance(data, list):
        return jsonify({'error': 'Data must be a list of servers'}), 400

    new_servers = []
    required_fields = ['country', 'city', 'flag', 'isFree', 'IP', "description", "category"]

    for server_data in data:
        # Verify that each server contains all required fields
        if not all(field in server_data for field in required_fields):
            return jsonify({'error': 'One or more servers are missing required fields'}), 400

        # Check if a server with the same IP already exists
        existing_server = Server.query.filter_by(IP=server_data['IP']).first()
        if existing_server:
            return jsonify({'error': f"Server with IP {server_data['IP']} already exists"}), 400

        # Create a new Server instance
        parsed_url = urlparse(server_data["IP"])

        ip_address = parsed_url.hostname
        print(ip_address)
        metadata = get_meta_data(ip_address)
        if (metadata == "error"):
            return jsonify({'error': 'problem get metadata'}), 400
        new_server = Server(
            country=server_data['country'],
            city=server_data['city'],
            flag=server_data['flag'],
            IP=server_data["IP"],
            isFree=server_data['isFree'],
            description=server_data['description'],
            category=server_data["category"],
            latitude=metadata["latitude"],
            longitude=metadata["longitude"],
            region=metadata["region"],
            postal=metadata["postal"]
        )
        # print(new_server)

        new_servers.append(new_server)

    try:
        for server in new_servers:
            db.session.add(server)
        db.session.commit()
        return jsonify({'message': f'{len(new_servers)} server(s) added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@server_bp.route('/server/<int:id>', methods=['DELETE'])
def delete_server(id):
    server = Server.query.get_or_404(id)
    db.session.delete(server)
    db.session.commit()
    return jsonify({'message': 'Server deleted successfully'})


@server_bp.route('/server/ip', methods=['DELETE'])
def delete_server_by_ip():
    data = request.json
    ip = data.get('ip')

    if not ip:
        return jsonify({'error': 'IP is required'}), 400

    server = Server.query.filter_by(IP=ip).first_or_404()
    try:
        db.session.delete(server)
        db.session.commit()
        return jsonify({'message': 'Server deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@server_bp.route('/server/ip', methods=['PUT'])
def update_server_ip():
    data = request.json
    old_ip = data.get('old_ip')
    new_ip = data.get('new_ip')

    if not old_ip or not new_ip:
        return jsonify({'error': 'Both old IP and new IP are required'}), 400

    existing_server = Server.query.filter_by(IP=new_ip).first()
    if existing_server:
        return jsonify({'error': 'Server with new IP already exists'}), 400

    server = Server.query.filter_by(IP=old_ip).first_or_404()
    try:
        server.IP = new_ip
        db.session.commit()
        return jsonify({'message': 'Server IP updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@server_bp.route("/config", methods=['POST'])
def get_config():
    data = request.json
    message = data["message"]
    public_key = data["public_key"]
    user = data["user"]
    user_infor = rsaRedis.get_user(username=user)
    private_key = user_infor["private_key"]
    try:
        decryptMessage = decrypt(private_key, message)
    except:
        return jsonify({"message": "error decrypt"}), 500
    result = get_user_and_server_id(decryptMessage)
    if "error" in result:
        return jsonify({"message": "can't get config file"}), 404
    server = Server.query.filter_by(id=result["server_id"]).first()

    wireguard_config=""
    try:
        wireguard_config=get_wireguard(server.IP,result["user"])
        if(wireguard_config=="error"):
            return jsonify({'message':"full"}),404
        private_key_line = re.search(r'(PrivateKey\s*=\s*[^\n]+)', wireguard_config).group(1)
        address_line = re.search(r'(Address\s*=\s*[^\n]+)', wireguard_config).group(1)
        DNS_line = re.search(r'(DNS\s*=\s*[^\n]+)', wireguard_config).group(1)
        public_key_line = re.search(r'(PublicKey\s*=\s*[^\n]+)', wireguard_config).group(1)
        endpoint_line = re.search(r'(Endpoint\s*=\s*[^\n]+)', wireguard_config).group(1)
        AllowedIPs_line=re.search(r'(AllowedIPs\s*=\s*[^\n]+)', wireguard_config).group(1)
        PersistentKeepalive=re.search(r'(PersistentKeepalive\s*=\s*[^\n]+)', wireguard_config).group(1)
        encryptMessage1=encrypt(public_key,f"{private_key_line}\n{address_line}")
        encryptMessage2=encrypt(public_key,f"{public_key_line}\n{public_key_line}")
        encryptMessage = f"{encryptMessage1}\t{encryptMessage2}"
        wireguard_config = f"""
        [Interface]
encryptMessage1
{DNS_line}
[Peer]
encryptMessage2
{endpoint_line}
{AllowedIPs_line}
{PersistentKeepalive}
        """
        return jsonify({
            "certificate": encryptMessage,
            "config": wireguard_config
        }), 200
    except Exception as e:
        print({"message": str(e)})
        return jsonify({"message":"server down"}),503

