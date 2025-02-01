from flask import Blueprint, request, jsonify,send_file
from models import db, rsaRedis,Server
from services.server_services import createClient,get_ovpn
from services.rsa_services import generate_rsa_key_pair,encrypt,decrypt
from services.format_check import get_user_and_server_id,get_certificate
server_bp = Blueprint('server_bp', __name__)

@server_bp.route('/listServer', methods=['GET'])
def get_servers():
    servers = Server.query.all()
    return jsonify([
        {
            'id': server.id,
            'country': server.country,
            'city':server.city,
            'flag': server.flag,
            'isFree': server.isFree,
            'IP': server.IP
        } for server in servers
    ])

@server_bp.route('/server', methods=['POST'])
def add_server():
    data = request.json
    existing_server = Server.query.filter_by(IP=data['IP']).first()

    if existing_server:
        return jsonify({'error': 'Server with this IP already exists'}), 400

    new_server = Server(
        country=data['country'],
        city=data['city'],
        flag=data['flag'],
        isFree=data['isFree'],
        IP=data['IP']
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
    required_fields = ['country', 'city', 'flag', 'isFree', 'IP']

    for server_data in data:
        # Verify that each server contains all required fields
        if not all(field in server_data for field in required_fields):
            return jsonify({'error': 'One or more servers are missing required fields'}), 400

        # Check if a server with the same IP already exists
        existing_server = Server.query.filter_by(IP=server_data['IP']).first()
        if existing_server:
            return jsonify({'error': f"Server with IP {server_data['IP']} already exists"}), 400

        # Create a new Server instance
        new_server = Server(
            country=server_data['country'],
            city=server_data['city'],
            flag=server_data['flag'],
            isFree=server_data['isFree'],
            IP=server_data['IP']
        )
        new_servers.append(new_server)

    # Add the list of new servers to the database
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

@server_bp.route("/config",methods=['POST'])
def get_config():
    data = request.json
    message=data["message"]
    public_key=data["public_key"]
    user=data["user"]
    user_infor=rsaRedis.get_user(username=user)
    private_key=user_infor["private_key"]
    decryptMessage=decrypt(private_key,message)
    print(decryptMessage)
    result = get_user_and_server_id(decryptMessage)
    if "error" in result:
        return jsonify({"message":"can't get config file"}),404
    print(f"result:{result}")
    server = Server.query.filter_by(id=result["server_id"]).first()
    print(server)
    createClient(server.IP,result["user"])
    ovpn_file_path=get_ovpn(server.IP,result["user"])
    print(f"opvnfile:{ovpn_file_path}")
    if(ovpn_file_path=="error"):
        return jsonify({'message':"full"}),404
    try:
        with open(ovpn_file_path, 'r') as file:
            content = file.read()
            # print(content)
            certificate=get_certificate(content).split("\n")[0]
            encryptMessage=encrypt(public_key,certificate)
            content=content.replace(certificate,"stringhasbeenencypt")
        return jsonify({
            "certificate":encryptMessage,
            "config": content
        }),200
    except Exception as e:
        return jsonify({"error": f"Error reading file: {str(e)}"}), 500