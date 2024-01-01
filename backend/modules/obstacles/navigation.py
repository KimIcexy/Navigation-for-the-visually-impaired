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
    def __init__(self, height_image=640, width_image=480):
        self.size = (height_image, width_image)
        self.obj_detection = None
        self.floor_detection = None
        self.depth_converter = None

    def init(self):
        self.obj_detection = ObjectDetection()
        self.floor_detection = FloorDetection()
        self.depth_converter = MakeDepthImage(self.size[0], self.size[1])
        
    def run(self, image, path):
        print('Obstacle detection...')
        obstacle_region = self.obj_detection.run(image)
        print(obstacle_region)
        
        print('Floor detection...')
        floor_region = self.floor_detection.run(image)
        print(floor_region)
        
        print('RGB >> depth...')
        depth_image = self.depth_converter.run(image)
        print(depth_image.shape)
        
        print('Path planning...')
        path_planning = PathPlanning(depth_image, obstacle_region[0], floor_region, path)
        if path_planning.goal == None:
            print('Cannot find path !!!')
            return None
        else:
            # make the old goal (if available) to be a start point for the next path planning
            path += path_planning.search_path()
            path = path_planning.optimize_path(path, 15)
            # self.show_results(path, image)
            return path_planning.get_results(image, path)

    def show_results(self, path, image):
        rgb_image = image.copy()
        # show path
        if path:
            print('path: ', path[:15], '...', path[-15:])
            for pixel in path:
                # coords = pixel.coords
                # print(coords)
                cv2.circle(rgb_image, pixel, 10, (255,255,255), -1)
        plt.imshow(rgb_image)
        plt.axis('off')  # Turn off axis labels
        plt.savefig('RESULT.jpg')
        
navigation = Navigation()