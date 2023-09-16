import jwt
from datetime import datetime

def generate_token(user_id):
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y %H:%M:%S")
    return jwt.encode({'user_id':user_id, 'time':current_time}, 'generate_token', algorithm='HS256')

def password_encode(password):
    return jwt.encode({'password':password}, 'hd', algorithm='HS256')

def password_decode(encoded_password):
    decoded = jwt.decode(encoded_password, 'hd', algorithms='HS256')
    return decoded['password']
