import sys
from flask import Blueprint, jsonify, request, g
import jwt
from db import get_db

from modules.users.models import User

bp = Blueprint('user', __name__, url_prefix='/api/')

@bp.route('/register/', methods=['POST'])
def register():
    data = request.get_json()

    if data['password'] != data['confirmPassword']:
        return jsonify({'message': 'Password does not match.'}), 400
    
    # Get database
    db = get_db()

    user = db.query(User).filter_by(username=data['username']).first()
    if user is not None:
        return jsonify({'message': 'Username already exists.'}), 400

    try:
        user = User(data)
        db.add(user)
        db.commit()
    except NameError:
        print(sys.exc_info()[0])
        db.rollback()
        return jsonify({'message': 'Register failed.'}), 400

    return jsonify({'message': 'Registered.'})


@bp.route('/login/', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    try:
        user = db.query(User).filter_by(username=data['username']).first()
    except NameError:
        print(sys.exc_info()[0])

        return jsonify({'message': 'Login failed.'}), 400

    print(user)
    if user is None:
        return jsonify({'message': 'Account not found.'}), 400
    print(user)

    if not user.verify_password(data['password']):
        return jsonify({'message': 'Wrong password.'}), 400

    token = jwt.encode({
        'id': user.id,
    }, getenv('SECRET_KEY'))

    return jsonify({'message': 'Logged in.', 'token': token}), 201