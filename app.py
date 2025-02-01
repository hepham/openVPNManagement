from flask import Flask
from models import db, init_db
from controllers.server_controller import server_bp
from controllers.rsa_controller import rsa_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///servers.db'

db.init_app(app)
app.register_blueprint(server_bp)
app.register_blueprint(rsa_bp)
if __name__ == '__main__':
    init_db(app)
    app.run(host='0.0.0.0', port=4000)