from flask import Blueprint, jsonify, request
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

from database.db import db
from modules.users.models.user_model import User
from utils.auth import token_required
from utils.image import base64_to_image, image_to_base64, one_face_valid

bp = Blueprint('face', __name__, url_prefix='/face/')

@bp.route('/valid/', methods=['POST'])
@token_required
def valid(current_user):
    '''
    Check if the image has only one face.
    '''
    form = request.form
    data = form['base64']
    
    image = base64_to_image(data)

    number_of_face, result = one_face_valid(image)

    if number_of_face == -1:
        return jsonify({'message': result}), 400
    elif number_of_face == 0:
        return jsonify({'message': 'No face detected!'}), 400
    elif number_of_face > 1:
        return jsonify({'message': 'More than one face detected!'}), 400
    
    # Convert image to base64
    image_base64 = image_to_base64(result)

    return jsonify({'image': image_base64}), 200

@bp.route('/register/', methods=['POST'])
@token_required
def accept_face(current_user):
    '''
    Accept the face. With one more valid.
    Bravo the 'don't trust the client' principle.
    '''
    form = request.form
    data = form['base64']

    image = base64_to_image(data)
    number_of_face, result = one_face_valid(image)

    # Since if this image is invalid then there's must be something wrong with the client.
    # Not because of the user, so there won't be many error messages.
    if number_of_face != 1:
        return jsonify({'message': 'Invalid image!'}), 400
    
    # Get face's embedding vector
    # TODO
    
    # Update face
    print(current_user)
    filters = {
        'id': current_user.id,
    }
    user = db.query(User, filters)[0]
    user.face_vector = data # Base64 image rather than, uhm, whatever cv2 uses.
    db.save(user)

    return jsonify({'message': 'Face registered!'}), 200