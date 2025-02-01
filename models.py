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


class RSARedis:
    def __init__(self):
        self.redis = get_redis_connection()

    def add_user(self, username, public_key, private_key):
        """Thêm user vào Redis với public và private key."""
        key = f"vpn_user:{username}"
        user_data = {
            "username": username,
            "public_key": public_key,
            "private_key": private_key
        }
        self.redis.hmset(key, user_data)
        self.redis.expire(key, 86400)  # Hết hạn sau 1 ngày

    def get_user(self, username):
        """Lấy thông tin user từ Redis."""
        key = f"vpn_user:{username}"
        if self.redis.exists(key):
            return self.redis.hgetall(key)
        return None

    def delete_user(self, username):
        """Xóa user khỏi Redis."""
        key = f"vpn_user:{username}"
        self.redis.delete(key)

    def get_all_users(self):
        """Lấy danh sách tất cả user đang kết nối."""
        keys = self.redis.keys("vpn_user:*")
        users = []
        for key in keys:
            users.append(self.redis.hgetall(key))
        return users

def init_db(app):
    with app.app_context():
        db.create_all()
rsaRedis=RSARedis()