import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def preprocess_image(image_path):
    # Read image
    image = Image.open(image_path)
    image = np.array(image).astype('uint8')  # Convert to uint8 data type

    # Split the RGB channels
    b, g, r = cv2.split(image)

    # Apply histogram equalization to each channel separately
    b_eq = cv2.equalizeHist(b)
    g_eq = cv2.equalizeHist(g)
    r_eq = cv2.equalizeHist(r)

    # Merge the equalized channels back into an RGB image
    equalized_image = cv2.merge((b_eq, g_eq, r_eq))

    # Display the original and equalized images using matplotlib
    plt.figure(figsize=(8, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title('Original Image')

    plt.subplot(1, 2, 2)
    plt.imshow(equalized_image)
    plt.title('Equalized Image')

    plt.show()

    return equalized_image

preprocess_image('16.jpg')