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
        return jsonify({'message': 'Mật khẩu không trùng khớp.'}), 400

    # Check with filters
    filters = {
        'username': data['username'],
    }
    user = db.query(User, filters)
    if user is not None and user != []:
        return jsonify({'message': 'Tài khoản đã tồn tại.'}), 400

    try:
        user = User(data)
    except AssertionError:
        return jsonify({'message': 'Thông tin người dùng không phù hợp.'}), 400
    
    try:
        db.save(user)
    except NameError:
        print(sys.exc_info()[0])
        db.rollback()
        return jsonify({'message': 'Đăng ký thất bại.'}), 400

    return jsonify({'message': 'Đăng ký thành công.'})


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

        return jsonify({'message': 'Đăng nhập thất bại.'}), 400

    if user is None or user == []:
        return jsonify({'message': 'Tài khoản không tồn tại.'}), 400

    user = user[0]

    if not user.verify_password(data['password']):
        return jsonify({'message': 'Sai mật khẩu.'}), 400

    token = jwt.encode({
        'id': user.id,
    }, SECRET_KEY)

    return jsonify({'message': 'Đăng nhập thành công.', 'token': token, 'user': user.simple_user()}), 201