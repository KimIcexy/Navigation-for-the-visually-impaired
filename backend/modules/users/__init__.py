import sys
from flask import Blueprint, jsonify, request
import jwt

from modules.users.models.user_model import User
from database.db import db
from utils.config import SECRET_KEY
from modules.users.module.image import bp as image_bp
from utils.image import base64_to_image, image_to_base64, one_face_valid

bp = Blueprint('user', __name__, url_prefix='/api/')
bp.register_blueprint(image_bp)

@bp.route('/register/', methods=['POST'])
def register():
    data = request.get_json()
    print(data)

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
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({'message': 'Đăng nhập thành công.', 'token': token, 'user': user.simple_user()}), 201

@bp.route('/login/face/', methods=['POST'])
def login_with_face():
    form = request.form
    data = form['base64']

    image = base64_to_image(data)
    number_of_face, result = one_face_valid(image)

    # Since if this image is invalid then there's must be something wrong with the client.
    # Not because of the user, so there won't be many error messages.
    if number_of_face == -1:
        return jsonify({'message': result}), 400
    if number_of_face != 1:
        message = 'Khuôn mặt không phù hợp! Ảnh có ' + str(number_of_face) + ' khuôn mặt'
        return jsonify({'message': message}), 400
    
    filters = {
        'username': form['username']
    }

    try:
        user = db.query(User, filters)
    except NameError:
        print(sys.exc_info()[0])
        return jsonify({'message': 'Đăng nhập thất bại.'}), 400
    
    if user is None or user == []:
        return jsonify({'message': 'Tài khoản không tồn tại.'}), 400
    
    user = user[0]

    if user.face_vector is None:
        return jsonify({'message': 'Tài khoản không tồn tại khuôn mặt.'}), 400

    if not user.verify_face(image):
        return jsonify({'message': 'Khuôn mặt không trùng khớp.'}), 400
    
    token = jwt.encode({
        'id': user.id,
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({'message': 'Đăng nhập thành công.', 'token': token, 'user': user.simple_user()}), 201