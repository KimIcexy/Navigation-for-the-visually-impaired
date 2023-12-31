import cv2
import os
import numpy as np
import tensorflow.compat.v1 as tf
from matplotlib import pyplot as plt
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg

# import models
from .models.fcrn import ResNet50UpProj

class MakeDepthImage:
    def __init__(self, height=1920, width=1080):
        tf.disable_eager_execution()
        self.sess = tf.Session()
        
        # Create a placeholder for the input image
        channels = 3
        batch_size = 1
        self.width = width
        self.height = height
        self.input_node = tf.placeholder(tf.float32, shape=(None, height, width, channels))

        # Construct the network
        self.net = ResNet50UpProj({'data': self.input_node}, batch_size, 1, False)

        # Load the converted parameters
        print('Loading the model')
        current_path = os.path.dirname(__file__)
        model_path = os.path.join(current_path, 'checkpoints', 'NYU_ResNet-UpProj.npy')
        self.net.load(model_path, self.sess)
    
    def preprocess_image(self, image):
        # Read image
        # image = Image.open(image_path)
        # image = np.array(image).astype('float32')
        image = np.expand_dims(np.asarray(image), axis = 0)
        return image
        
    def predict(self, image):
        with self.sess.as_default():
            # Evalute the network for the given image
            pred = self.sess.run(self.net.get_output(), feed_dict={self.input_node: image})
            
            # Plot result
            fig = plt.figure()
            ii = plt.imshow(pred[0,:,:,0], cmap='gray', interpolation='nearest')
            plt.axis('off')
            result_path = 'DEPTH_IMAGE.jpg'
            plt.savefig(result_path, bbox_inches='tight', pad_inches=0)
            plt.close()
            depth_image = cv2.imread(result_path, cv2.IMREAD_GRAYSCALE)
            depth_image = cv2.resize(depth_image, (self.width, self.height))
            return depth_image
    
    def test(self, rgb_image, no_frame):
        preprocessed_image = self.preprocess_image(rgb_image)
        with self.sess.as_default():
            # Evalute the network for the given image
            pred = self.sess.run(self.net.get_output(), feed_dict={self.input_node: preprocessed_image})
            
            # Plot result
            fig = plt.figure()
            ii = plt.imshow(pred[0,:,:,0], cmap='gray', interpolation='nearest')
            plt.axis('off')
            result_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            result_path = os.path.join(os.path.dirname(result_path), 'results', 'depth', f'{no_frame}.jpg')
            print('depth path: ', result_path)
            plt.savefig(result_path, bbox_inches='tight', pad_inches=0)
            plt.close()
            depth_image = cv2.imread(result_path, cv2.IMREAD_GRAYSCALE)
            depth_image = cv2.resize(depth_image, (self.width, self.height))
            return depth_image
        
    def run(self, rgb_image):
        return self.predict(self.preprocess_image(rgb_image))    