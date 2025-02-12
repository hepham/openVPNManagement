from flask_sqlalchemy import SQLAlchemy
import redis
from config import get_redis_connection
db = SQLAlchemy()

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    city=db.Column(db.String(500),nullable=False)
    flag = db.Column(db.String(200), nullable=False)
    isFree = db.Column(db.Boolean, default=True)
    IP = db.Column(db.String(100), nullable=False)
    description=db.Column(db.String(1000),nullable=False)
    category=db.Column(db.String(1000),nullable=False)
    latitude=db.Column(db.String(1000),nullable=True)
    longitude=db.Column(db.String(1000),nullable=True)
    region=db.Column(db.String(1000),nullable=True)
    postal=db.Column(db.String(1000),nullable=True)
    def __str__(self):
        return f"Server(id={self.id}, country={self.country}, city={self.city}, IP={self.IP}, isFree={self.isFree}, category={self.category},description={self.description})"

class RSARedis:
    def __init__(self):
        self.redis = get_redis_connection()

    def add_user(self, username, public_key, private_key):
        key = f"vpn_user:{username}"
        user_data = {
            "username": username,
            "public_key": public_key,
            "private_key": private_key
        }
        self.redis.hmset(key, user_data)
        self.redis.expire(key, 86400)

    def get_user(self, username):
        key = f"vpn_user:{username}"
        if self.redis.exists(key):
            return self.redis.hgetall(key)
        return None

    def delete_user(self, username):
        key = f"vpn_user:{username}"
        self.redis.delete(key)

    def get_all_users(self):
        keys = self.redis.keys("vpn_user:*")
        users = []
        for key in keys:
            users.append(self.redis.hgetall(key))
        return users

def init_db(app):
    with app.app_context():
        db.create_all()
rsaRedis=RSARedis()