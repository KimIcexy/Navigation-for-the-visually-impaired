import sys
from flask import Blueprint, jsonify, request
import jwt

from modules.users.models.user_model import User
from database.db import db

bp = Blueprint('user', __name__, url_prefix='/api/')

@bp.route('/register/', methods=['POST'])
def register():
    data = request.get_json()

    if data['password'] != data['confirmPassword']:
        return jsonify({'message': 'Password does not match.'}), 400

    # Check with filters
    filters = {
        'username': data['username'],
    }
    user = db.query(User, filters)
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
    db = g.db

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