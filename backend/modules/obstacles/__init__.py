import cv2
import os
import matplotlib.pyplot as plt

from .detect import ObjectDetection
from .detect.floor_detect import FloorDetection
from .navigate.path_planning import PathPlanning
from .navigate.rgb2depth import MakeDepthImage

class Navigation:
    # TODO later: solve problem which user's token of the image 
    # reuse previous results...
    def __init__(self, height_image=1920, width_image=1080) -> None:
        self.obj_detection = ObjectDetection()
        self.floor_detection = FloorDetection()
        self.depth_converter = MakeDepthImage(height_image, width_image)
        self.user_token = None # use later 
        self.path = []
        
    def run(self, image):
        print('Obstacle detection...')
        obstacle_region = self.obj_detection.run(image)
        
        print('Floor detection...')
        floor_region = self.floor_detection.run(image)
        
        print('RGB >> depth...')
        depth_image = self.depth_converter.run(image)

        print('Path planning...')
        path_planning = PathPlanning(depth_image, obstacle_region[0], floor_region, self.path)
        if path_planning.goal == None:
            print('Cannot find path !!!')
            return None
        else:
            # make the old goal (if available) to be a start point for the next path planning
            start_point = path_planning.goal.coords
            self.path += path_planning.search_path()
            # self.path = path_planning.optimize_path(path, 15)
            return path_planning.get_results(image, self.path)
