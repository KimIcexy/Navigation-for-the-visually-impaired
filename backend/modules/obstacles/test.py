import cv2
import os
import matplotlib.pyplot as plt

from detect import ObjectDetection
from detect.floor_detect import FloorDetection
from navigate.path_planning import PathPlanning
# from navigate.rgb2depth import MakeDepthImage


obj_detection = ObjectDetection()
floor_detection = FloorDetection()
# depth_converter = MakeDepthImage()
start = 1
stop = 10
n_frames = 16
frames_path = 'test_resources/frames'

for frame in range(start, stop):
    # frame = i * n_frames
    print('\nFrame: ', frame)
    frame_path = os.path.join(frames_path, str(frame)+'.jpg')
    # print('frame_path: ', frame_path)
    
    """Test object detection"""
    print('Obstacle detection...')
    obstacle_region = obj_detection.run(frame_path, frame)
    # print('Obstacles: ', obstacle_region[0])

    """Test navigation"""
    print('Floor detection...')
    floor_region = floor_detection.run(frame_path, frame)
    
    """Test depth converter"""
    print('RGB >> depth...')
    # nhớ mở comment ở trên depth_image class và import depth image ...
    # depth_image = depth_converter.run(frame_path, frame)
    
    """for faster test, read from result image"""
    depth_image_path = os.path.join('results/depth', str(frame) + '.jpg')
    depth_image = cv2.imread(depth_image_path, cv2.IMREAD_GRAYSCALE)
    depth_image = cv2.resize(depth_image, (1080, 1920))
        
    """Test path planning"""
    print('Path planning...')
    path_planning = PathPlanning(depth_image, obstacle_region[0], floor_region)
    if path_planning.goal == None:
        print('Cannot find path !!!')
    else:
        path = path_planning.search_path()
        # print('Path: ', path)
        path_planning.show_result(obstacle_region, path, frame)
    