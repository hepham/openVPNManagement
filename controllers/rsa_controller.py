from flask import Blueprint, request, jsonify,send_file
from models import db, rsaRedis
from services.rsa_services import generate_rsa_key_pair,encrypt,decrypt
saveKey={}
rsa_bp = Blueprint('rsa_bp', __name__)
@rsa_bp.route('/key/<string:username>', methods=['GET'])
def get_key(username):
    private_key,public_key=generate_rsa_key_pair()
    rsaRedis.add_user(username=username,public_key=public_key,private_key=private_key)
    return jsonify({"key":public_key}),201

@rsa_bp.route("/key/all", methods=["GET"])
def get_all():
    print(rsaRedis.get_all_users())
    return jsonify({"message": "Ok"}), 200