import sys
from flask import Blueprint, jsonify, request

from utils.image import base64_to_image
from utils.auth import token_required
from modules.obstacles.navigation import navigation

bp = Blueprint('obstacles', __name__)

@bp.route('/navigate/', methods=['POST'])
@token_required
def navigate(current_user):
    form = request.form
    data = form['base64']
    
    image = base64_to_image(data)

    try:
        results = navigation.run(image)
        print('results: ', results)
        jsonify({'results': results}), 200
    except Exception as e:
        print('Unexpected error:', e)
        jsonify({'message': 'Error'}), 400
