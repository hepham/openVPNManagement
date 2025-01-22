from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    flag = db.Column(db.String(200), nullable=False)
    isFree = db.Column(db.Boolean, default=True)
    IP = db.Column(db.String(100), nullable=False)

def init_db(app):
    with app.app_context():
        db.create_all()
