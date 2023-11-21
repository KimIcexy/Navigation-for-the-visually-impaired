import sys
from flask import Blueprint, jsonify, request
import jwt

from modules.users.models.user_model import User
from database.db import db
from utils.config import SECRET_KEY

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
    if user is not None and user != []:
        return jsonify({'message': 'Username already exists.'}), 400

    try:
        user = User(data)
    except AssertionError:
        return jsonify({'message': 'User is not valid.'}), 400
    
    try:
        db.save(user)
    except NameError:
        print(sys.exc_info()[0])
        db.rollback()
        return jsonify({'message': 'Register failed.'}), 400

    return jsonify({'message': 'Registered.'})


@bp.route('/login/', methods=['POST'])
def login():
    data = request.get_json()

    filters = {
        'username': data['username'],
    }
    try:
        user = db.query(User, filters)
    except NameError:
        print(sys.exc_info()[0])

        return jsonify({'message': 'Login failed.'}), 400

    if user is None or user == []:
        return jsonify({'message': 'Account not found.'}), 400

    user = user[0]

    if not user.verify_password(data['password']):
        return jsonify({'message': 'Wrong password.'}), 400

    token = jwt.encode({
        'id': user.id,
    }, SECRET_KEY)

    return jsonify({'message': 'Logged in.', 'token': token, 'user': user.simple_user()}), 201