import argparse
import os
import numpy as np
import tensorflow.compat.v1 as tf
from matplotlib import pyplot as plt
from PIL import Image

import models

def predict(model_data_path, image_path, result_path):
    # Default input size
    height = 228
    width = 304
    channels = 3
    batch_size = 1
   
    # Read image
    img = Image.open(image_path)
    img = img.resize([width,height], Image.Resampling.LANCZOS)
    img = np.array(img).astype('float32')
    img = np.expand_dims(np.asarray(img), axis = 0)
   
    # Create a placeholder for the input image
    input_node = tf.placeholder(tf.float32, shape=(None, height, width, channels))

    # Construct the network
    net = models.ResNet50UpProj({'data': input_node}, batch_size, 1, False)
        
    with tf.Session() as sess:

        # Load the converted parameters
        print('Loading the model')

        # Use to load from ckpt file
        # saver = tf.train.Saver()     
        # saver.restore(sess, model_data_path)

        # Use to load from npy file
        net.load(model_data_path, sess) 

        # Evalute the network for the given image
        pred = sess.run(net.get_output(), feed_dict={input_node: img})
        
        # Plot result
        fig = plt.figure()
        ii = plt.imshow(pred[0,:,:,0], cmap='gray', interpolation='nearest')
        plt.axis('off')
        # plt.axis('equal')  # Set equal aspect ratio
        plt.savefig(result_path, bbox_inches='tight', pad_inches=0)
        plt.show()
        
        return pred
        
                
def main():
    # Parse arguments
    # parser = argparse.ArgumentParser()
    # parser.add_argument('model_path', help='Converted parameters for the model')
    # parser.add_argument('image_paths', help='Directory of images to predict')
    # args = parser.parse_args()

    # Predict the image
    model_path = './checkpoints/NYU_ResNet-UpProj.npy'
    image_path = './test.jpg'
    result_path = './result.png'
    print('RGB >> depth...')
    tf.disable_eager_execution()
    pred = predict(model_path, image_path, result_path)
    
    # os._exit(0)

if __name__ == '__main__':
    main()

        



