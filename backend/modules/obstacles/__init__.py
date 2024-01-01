import sys
from flask import Blueprint, jsonify, request

from utils.image import base64_to_image
from utils.auth import token_required
from modules.obstacles.navigation import navigation
from backend.utils.paths import paths

bp = Blueprint('obstacles', __name__)

@bp.route('/navigate/', methods=['POST'])
@token_required
def navigate(current_user):
    form = request.form
    data = form['base64']
    
    image = base64_to_image(data)
    try:
        # get paths[current_user.username] or create the empty result (if not exist)
        path = paths.setdefault(current_user.username, [])
        
        # navigation based on the input image and update the path
        results = navigation.run(image, path)
        
        print('results: ', results)
        print('user path len: ', len(path))
        jsonify({'results': results}), 200
    except Exception as e:
        print('Unexpected error:', e)
        jsonify({'message': 'Error'}), 400
