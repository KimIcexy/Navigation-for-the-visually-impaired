import sys
from flask import Blueprint, jsonify, request

from utils.image import base64_to_image
from utils.auth import token_required

bp = Blueprint('obstacles', __name__)

@bp.route('/navigate/', methods=['POST'])
@token_required
def navigate(current_user):
    form = request.form
    data = form['base64']
    
    image = base64_to_image(data)

    return jsonify({'message': 'OK'}), 200