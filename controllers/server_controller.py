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
            'category':server.category,
            'description':server.description,
            "IP":server.IP
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
            IP=data["IP"],
            isFree=data['isFree'],
            description=data['description'],
            category=data["category"]
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
    required_fields = ['country', 'city', 'flag', 'isFree', 'IP',"description","category"]

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
            IP=server_data["IP"],
            isFree=server_data['isFree'],
            description=server_data['description'],
            category=server_data["category"]
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

@server_bp.route("/config",methods=['POST'])
def get_config():
    data = request.json
    message=data["message"]
    public_key=data["public_key"]
    user=data["user"]
    user_infor=rsaRedis.get_user(username=user)
    private_key=user_infor["private_key"]
    try:
        decryptMessage=decrypt(private_key,message)
    except:
        return jsonify({"message":"error decrypt"}),500
    result = get_user_and_server_id(decryptMessage)
    if "error" in result:
        return jsonify({"message":"can't get config file"}),404
    server = Server.query.filter_by(id=result["server_id"]).first()
    ovpn_config=get_ovpn(server.IP,result["user"])
    if(ovpn_config=="error"):
        return jsonify({'message':"full"}),404
    try:

        certificate=get_certificate(ovpn_config).split("\n")[0]
        encryptMessage=encrypt(public_key,certificate)
        ovpn_config=ovpn_config.replace(certificate,"stringhasbeenencypt")
        return jsonify({
            "certificate":encryptMessage,
            "config": ovpn_config
        }),200
    except Exception as e:
        return jsonify({"error": f"Error reading file: {str(e)}"}), 500