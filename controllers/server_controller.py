from flask import Blueprint, request, jsonify,send_file
from models import db, Server
from services.server_services import createClient,get_ovpn
server_bp = Blueprint('server_bp', __name__)

@server_bp.route('/listServer', methods=['GET'])
def get_servers():
    servers = Server.query.all()
    return jsonify([
        {
            'id': server.id,
            'country': server.country,
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
        flag=data['flag'],
        isFree=data['isFree'],
        IP=data['IP']
    )
    db.session.add(new_server)
    db.session.commit()
    return jsonify({'message': 'Server added successfully'}), 201

@server_bp.route('/server/<int:id>', methods=['DELETE'])
def delete_server(id):
    server = Server.query.get_or_404(id)
    db.session.delete(server)
    db.session.commit()
    return jsonify({'message': 'Server deleted successfully'})

@server_bp.route("/config",methods=['POST'])
def get_config():
    data = request.json
    server_id=data["server_id"]
    request_time=data["request_time"]
    time_encode=data["time_encode"]
    server = Server.query.filter_by(id=server_id).first()
    createClient(server.IP,request_time)
    ovpn_file_path=get_ovpn(server.IP,request_time)
    if(ovpn_file_path=="error"):
        return jsonify({'message':"full"}),404
    return send_file(ovpn_file_path, as_attachment=True, download_name=f"{request_time}.ovpn")