from flask import Flask, jsonify, request
import numpy as np
import base64
import cv2

from utils.config import *
from utils.database import Database
from modules.obstacles import *

app = Flask(__name__)
database = Database()

@app.route('/')
def home():
    try:
        database_connection = database.connect()
        return 'Hello, you have connected to the database~~~'
    except Exception as e:
        return str(e)
    
# Route for return predict result
@app.route('/navigation', methods=['POST'])
def navigation():
    try:
        #Convert base64 image to numpy array
        data = request.get_json()
        header, base64_image = data['image'].split(',', 1)
        image_bytes = base64.b64decode(base64_image)
        image_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        # TODO later: solve problem which user's token of the image 
        # reuse previous results...
        navigator = Navigation(image.shape[0], image.shape[1])
        results = navigator.run(image)
        print('results: ', results)
        return jsonify({'results': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=PORT)