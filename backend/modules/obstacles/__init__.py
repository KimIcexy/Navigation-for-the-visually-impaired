from flask import Blueprint, request, jsonify
import numpy as np

from utils.auth import token_required
from utils.image import base64_to_image

bp = Blueprint('navigate', __name__)

@bp.route('/navigate/', methods=['POST'])
@token_required
def navigate(current_user):
    print(request)
    form = request.form
    data = form['base64']
    image = base64_to_image(data)

    # DO SOMETHING HERE

    # Generating a random number of random bounding boxes
    # The number of bounding boxes is from 1 to 10
    n_boxes = np.random.randint(1, 10)

    # Generating random bounding boxes, with top-left coordinate and size
    # The bounding box must be inside the image
    boxes = []
    for i in range(n_boxes):
        x = np.random.randint(0, image.shape[1])
        y = np.random.randint(0, image.shape[0])
        w = np.random.randint(0, image.shape[1] - x)
        h = np.random.randint(0, image.shape[0] - y)
        boxes.append([x, y, w, h])

    return jsonify({'boxes': boxes}), 200