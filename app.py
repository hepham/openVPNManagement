import os
from flask import Flask
from models import db, init_db
from controllers.server_controller import server_bp
from controllers.rsa_controller import rsa_bp

app = Flask(__name__)

# Cấu hình ứng dụng
app.config.update(
    DEBUG=False,
    SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'sqlite:///servers.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY=os.getenv('SECRET_KEY', 'your-secret-key-here')
)

# Khởi tạo database và blueprints
db.init_app(app)
app.register_blueprint(server_bp)
app.register_blueprint(rsa_bp)

# Khởi tạo database khi ứng dụng khởi động
with app.app_context():
    init_db(app)