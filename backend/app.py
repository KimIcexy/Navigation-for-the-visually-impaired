from flask import Flask
import os
import psycopg2
import numpy as np
import base64
import cv2

from utils.config import *
from utils.database import Database

app = Flask(__name__)
database = Database()

@app.route('/')
def home():
    try:
        database_connection = database.connect()
        return 'Hello, you have connected to the database~~~'
    except Exception as e:
        return str(e)

@app.route('/predict')
def predict():
    #Convert base64 image to numpy array
    data = request.get_json()
    #You have to skip data:image/jpeg;base64, to get only base64
    # data which will give you correct image data and cv2 will
    # decode and display it.
    header, base64_image = data['image'].split(',', 1)
    image_bytes = base64.b64decode(base64_image)
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return str(image)

if __name__ == '__main__':
    app.run(debug=True, port=PORT)