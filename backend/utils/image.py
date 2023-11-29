import base64
import cv2
import numpy as np
from deepface import DeepFace

def one_face_valid(image):
    try:
        image_array = np.asarray(image)
    except Exception as e:
            # If the conversion fails, log the error and return the original image.
        return -1, 'Không thể chuyển đổi ảnh.'
    print(image_array.shape)
    
    try:
        faces = DeepFace.extract_faces(image_array, detector_backend='opencv')
    except Exception as e:
        # If the extractionn fails, log the error and return the original image.
        print(e)
        return -1, 'Không thể trích xuất khuôn mặt.'
    
    number_of_face = len(faces)
    if number_of_face != 1:
        return number_of_face, None
    
    # Draw face
    area = faces[0]['facial_area']
    x = area['x']
    y = area['y']
    w = area['w']
    h = area['h']
    new_image = np.asarray(image)
    cv2.rectangle(new_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return number_of_face, new_image

def image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer)
    return image_base64.decode('utf-8')

def base64_to_image(image_base64):
    image = base64.b64decode(image_base64)
    image = np.asarray(bytearray(image), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image