import argparse
import os
import numpy as np
import tensorflow.compat.v1 as tf
from matplotlib import pyplot as plt
from PIL import Image

import models

def predict(model_data_path, image_path, result_path):
    # Read image, convert to grayscale
    img = Image.open(image_path)

    # Default input size
    # width = 228
    # height = 304
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
    image_paths = ['./test/test1.jpg', './test/test2.jpg', './test/test3.jpg', './test/test4.jpg', './test/test5.jpeg']
    result_paths = ['./results/result1.jpg', './results/result2.jpg', './results/result3.jpg', './results/result4.jpg', './results/result5.jpg']
    print('RGB >> depth...')
    tf.disable_eager_execution()
    i = 0
    pred = predict(model_path, image_paths[i], result_paths[i])    
    os._exit(0)

if __name__ == '__main__':
    main()

        



