import cv2
import os
import numpy as np
import tensorflow.compat.v1 as tf
from matplotlib import pyplot as plt
from PIL import Image

# import models
from .models.fcrn import ResNet50UpProj

class MakeDepthImage:
    def __init__(self):
        pass
    
    def predict(self, image_path):
        # Read image, convert to grayscale
        img = Image.open(image_path)
        width = img.size[0]
        height = img.size[1]
        channels = 3
        batch_size = 1
    
        img = img.resize([width,height], Image.Resampling.LANCZOS)
        img = np.array(img).astype('float32')
        img = np.expand_dims(np.asarray(img), axis = 0)
    
        # Create a placeholder for the input image
        input_node = tf.placeholder(tf.float32, shape=(None, height, width, channels))

        # Construct the network
        net = ResNet50UpProj({'data': input_node}, batch_size, 1, False)
            
        with tf.Session() as sess:
            # Load the converted parameters
            print('Loading the model')
            # Use to load from npy file
            current_path = os.path.dirname(__file__)
            model_path = os.path.join(current_path, 'checkpoints', 'NYU_ResNet-UpProj.npy')

            net.load(model_path, sess) 

            # Evalute the network for the given image
            pred = sess.run(net.get_output(), feed_dict={input_node: img})
            
            # Plot result
            fig = plt.figure()
            ii = plt.imshow(pred[0,:,:,0], cmap='gray', interpolation='nearest')
            plt.axis('off')
            result_path = os.path.join(current_path, 'depth_image.png')
            plt.savefig(result_path, bbox_inches='tight', pad_inches=0)
            # plt.show()
            plt.close()
            depth_image = cv2.imread(result_path, cv2.IMREAD_GRAYSCALE)
            depth_image = cv2.resize(depth_image, (width,height))
            return depth_image
    
    def run(self, image_path):
        print('RGB >> depth...')
        tf.disable_eager_execution()
        return self.predict(image_path)    
        # os._exit(0)