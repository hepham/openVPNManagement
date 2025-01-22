from flask import Flask
from models import db, init_db
from controllers.server_controller import server_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///servers.db'

db.init_app(app)
app.register_blueprint(server_bp)

if __name__ == '__main__':
    init_db(app)
    app.run(port=3000,debug=True)
