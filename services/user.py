from db.models import User
import hashlib

def get_user(user_id):
    return User.read(user_id=user_id)

def save_user(user_object):
    user_object.hash_password = hashlib.sha256(user_object.hash_password.encode()).hexdigest()
    return User.write(user_object)

