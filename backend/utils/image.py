import base64
import cv2
import numpy as np
from deepface import DeepFace

def balance_brightness(img):
    yuv_img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    # Apply histogram equalization to the Y channel
    yuv_img[:,:,0] = cv2.equalizeHist(yuv_img[:,:,0])

    # Convert the image back to BGR color space
    balanced_img = cv2.cvtColor(yuv_img, cv2.COLOR_YUV2BGR)

    return balanced_img

def one_face_valid(image):
    try:
        image_array = np.asarray(image)
        # image_array = balance_brightness(image_array)
    except Exception as e:
            # If the conversion fails, log the error and return the original image.
        return -1, 'Không thể chuyển đổi ảnh.'
    
    print(image_array.shape)
    
    try:
        faces = DeepFace.extract_faces(image_array, detector_backend='retinaface')
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

def euclide_l2(face_1, face_2, threshold=0.65):
    def l2_normalize(x):
        return x / np.sqrt(np.sum(np.multiply(x, x)))
    face_1 = l2_normalize(face_1)
    face_2 = l2_normalize(face_2)
    
    def euclidean(x, y):
        euclide_distance = x - y
        euclide_distance = np.sum(np.multiply(euclide_distance, euclide_distance))
        euclide_distance = np.sqrt(euclide_distance)
        return euclide_distance
    
    result = euclidean(face_1, face_2)
    print(result)
    return result <= threshold