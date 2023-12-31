import cv2
import os
import matplotlib.pyplot as plt

from detect import ObjectDetection
from detect.floor_detect import FloorDetection
from navigate.path_planning import PathPlanning
from navigate.rgb2depth import MakeDepthImage


class Navigation:
    def __init__(self) -> None:
        self.obj_detection = ObjectDetection()
        self.floor_detection = FloorDetection()
        self.depth_converter = MakeDepthImage()
        self.user_token = None # use later 
        self.path = []
        
    # TODO later: solve problem which user's token of the frame 
    def run(self, image):
        print('Obstacle detection...')
        obstacle_region = self.obj_detection.run(frame_path, frame)
        
        print('Floor detection...')
        floor_region = self.floor_detection.run(frame_path, frame)
        
        print('RGB >> depth...')
        depth_image = self.depth_converter.run(frame_path, frame)

        print('Path planning...')
        path_planning = PathPlanning(depth_image, obstacle_region[0], floor_region, path)
        if path_planning.goal == None:
            print('Cannot find path !!!')
        else:
            # make the old goal to be a start point for the next path planning
            start_point = path_planning.goal.coords
            path += path_planning.search_path()
            print('Raw frame ' + str(frame) + ': ', path)
            if frame != 720:
                print ('Frame '+ str(frame) + ' Optimized')
                path = path_planning.optimize_path(path, 15)
            #print('Optimize path: ', path)
            path_planning.show_result(origin_image, path, frame)
    
