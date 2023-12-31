from flask import jsonify, request
from functools import wraps
import jwt

from modules.users.models.user_model import User
from utils.config import SECRET_KEY
from database import db

def token_required(func):
    '''
    Decorator function to check if user is logged in

    :param func: function to be decorated

    How to use:
    @token_required
    def function_to_be_decorated():
        pass
    '''
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]

        if not token or token == 'null':
            return jsonify({'message': 'Không tìm thấy token.'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            filter = {
                'id': data['id'],
            }
            current_user = db.query(User, filter)
        except:
            return jsonify({'message': 'Token không phù hợp'}), 401
        
        return func(current_user[0], *args, **kwargs)
    
    return wrapped_function