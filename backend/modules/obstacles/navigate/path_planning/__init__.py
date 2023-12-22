import numpy as np
import cv2
import math
from matplotlib import pyplot as plt

class PixelNode:
    """Node save information of each pixel in the image
    
    Attributes:
        coords: coordinate of this pixel (x, y)
        depth: depth value of this pixel
        walkable: True (not in obstacle area) or False (in obstacle area)
        cost: cost to go to this pixel
        neighbors: walkable node in adjacent pixels
        pre_node: previous pixel node (for backtracking path)
        total_cost: total cost from the start pixel to this pixel
    """
    
    def __init__(self, coords, depth, walkable, cost):
        self.coords = coords
        self.depth = depth
        self.walkable = walkable
        self.cost = cost
        self.neighbors = None 
        self.pre_node = None
        self.total_cost = math.inf
        
class PathPlanning:
    """Planning path using depth image and obstacle detection results
    Args:
        depth_image: depth image
        obstacle_region: bounding boxes and type of obstacles
        floor_region: bounding boxes of detected floor
        
    Atributes:
        depth_image: depth image
        walkable_map: map showing walkable or non-walkable pixel
        planning_map: map of PixelNode which used to path planning
        start: PixelNode that begin to path planning
        goal: PixelNode that the path planning want to reach        
    """  
    
    def __init__(self, depth_image, obstacle_region, floor_region):
        self.depth_image = depth_image
        # self.obstacle_region = self.read_obstacle_region(obstacle_region)
        self.walkable_map = self.create_walkable_map(obstacle_region, floor_region)
        self.planning_map = self.create_planning_map()
        point = self.find_start_point()
        self.start = self.planning_map[point[1], point[0]]
        self.start.total_cost = 0
        self.start.cost = 0
        print('Start coords: ', self.start.coords)
        point = self.make_temp_goal()
        print('Temp goal: ', point)
        self.goal = self.planning_map[point[1], point[0]]
        
    def read_obstacle_region(self, obstacle_region):
        # format: center coord: (bx, by), size (bw, bh) (normalized),
        # may need to change later based on the output format from the module 3 !!!
        bboxes = []
        for bbox in obstacle_region:
            x = int((float(bbox[0])-float(bbox[2])/2) *self.depth_image.shape[1]) # bx * width (n_columns)
            y = int((float(bbox[1])-float(bbox[3])/2) *self.depth_image.shape[0]) # by * height (n_rows)
            w = int(float(bbox[2])*self.depth_image.shape[1]) # bw * width
            h = int(float(bbox[3])*self.depth_image.shape[0]) # bh * height
            bboxes.append([x, y, w, h])
        return np.array(bboxes)
    
    def find_start_point(self):
        # start point: mid bottom point in the image
        x = int(self.depth_image.shape[1] / 2)
        y = int(self.depth_image.shape[0] - 1)
        return (x, y)
        # return (702, 971)
    
    def hard_code_temp_goal(self):
        return tuple(np.argwhere(self.walkable_map==True)[0])
    
    def make_temp_goal(self):
        longest_path = self.find_longest_path()
        temp_goal = self.find_path_center(longest_path)
        return temp_goal

    def find_longest_path(self):
        # using DFS algorithm
        stack = [self.start]
        visited = set()
        longest_path = []

        while stack:
            current_node = stack.pop()
            # print('current node: ', current_node)
            # print('current walkable: ', current_node.walkable)
            if current_node not in visited and current_node.walkable:
                visited.add(current_node)
                # print('visited len: ', len(visited))
                longest_path.append(current_node.coords)
                self.get_neighbors(current_node)
                neighbors = current_node.neighbors
                if neighbors is not None:
                    stack.extend(neighbors)
        return longest_path

    def find_path_center(self, path):
        if not path:
            return None
        center = int(len(path)/4 -1)
        return path[center]
    
    def create_planning_map(self):
        height, width = self.depth_image.shape[:2]
        planning_map = np.array([[None for _ in range(width)] for _ in range(height)])
        for y in range(height):
            for x in range(width):
                planning_map[y, x] = PixelNode(coords=(x, y),
                                    depth=self.depth_image[y, x],
                                    walkable=self.walkable_map[y, x],
                                    cost=255 - self.depth_image[y, x], # cost is opposite with depth value
                                    )
        return planning_map
    
    def create_walkable_map(self, obstacle_region, floor_region):
        walkable_map = np.zeros((self.depth_image.shape[0], self.depth_image.shape[1]), dtype=bool)
        for bbox in floor_region:
            # print(bbox)
            top, left, bottom, right = bbox[0], bbox[1], bbox[2], bbox[3]
            walkable_map[top:bottom+1, left:right+1] = True
        
        # bbox_margin = 10
        for obstacle in obstacle_region:
            bbox = obstacle[0]
            left, top, right, bottom = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            walkable_map[top:bottom+1, left:right+1] = False
        return walkable_map        
    
    def heuristic(self, pixel):
        goal_coords = self.goal.coords
        pixel_coords = pixel.coords
        return np.sqrt((goal_coords[0] - pixel_coords[0]) ** 2 + (goal_coords[1] - pixel_coords[1]) ** 2)

    def get_neighbors(self, current_node, neighbor_type='4'):
        # has not assign neighbors before
        if (current_node.neighbors is None):
            x, y = current_node.coords
            if (neighbor_type=='8'):
                neighbors = self.planning_map[max(y-1, 0):min(y+2, self.depth_image.shape[0]), \
                                            max(x-1, 0):min(x+2, self.depth_image.shape[1])]
                neighbors = neighbors.flatten()
                for i in range(neighbors.shape[0]):
                    if neighbors[i].coords == current_node.coords or \
                    not neighbors[i].walkable:
                        current_node.neighbors = np.delete(neighbors, i)
                    
            # neighbor_type='4':
            neighbors_row = self.planning_map[y, max(x-1, 0):min(x+2, self.depth_image.shape[1])].flatten()
            neighbors_col = self.planning_map[max(y-1, 0):min(y+1, self.depth_image.shape[0]), x].flatten()

            new_neighbors = np.concatenate((neighbors_col, neighbors_row))
            new_neighbors_list = []
            for neighbor in new_neighbors:
                if neighbor.coords != current_node.coords and neighbor.walkable:
                    new_neighbors_list.append(neighbor)
            current_node.neighbors = np.array(new_neighbors_list)
        
    def search_path(self):
        # use A* search algorithm from start to goal
        open_set = [self.start]
        closed_set = set()
        # print('start node: ', self.start.coords)
        # print('end node: ', self.goal.coords)
        
        while open_set:
            for node in open_set:
                # find the node with the least cost + heuristic value on the open_set:
                current_node = open_set[0]
                if node.total_cost + self.heuristic(node) < current_node.total_cost + self.heuristic(current_node):
                    current_node = node
                # if current_node is the goal, backtracking and return the path
                if current_node == self.goal:
                    print('reach goal')
                    pre_node = current_node.pre_node
                    path = []
                    while pre_node:
                        path.insert(0, pre_node)
                        pre_node = pre_node.pre_node
                    return path
                
                # pop the current_node out of the open_set:
                open_set.remove(current_node)
                
                # assign neighbors for current_node:
                self.get_neighbors(current_node)
                
                # traverse all neighbors of current_node:
                # print('current_node: ', current_node.coords)
                for neighbor in current_node.neighbors:
                    if neighbor not in closed_set and \
                        current_node.total_cost + neighbor.cost < neighbor.total_cost:
                            # update the shorter total_cost:
                            neighbor.total_cost = current_node.total_cost + neighbor.cost
                            # set neighbors' pre_node of current_node is current_node:
                            neighbor.pre_node = current_node
                            if neighbor not in open_set:
                                open_set.append(neighbor)
                        
                # add current_node to the closed set:
                closed_set.add(current_node)        
    
    def show_result(self, obstacle_region, path, i=1):
        temp_image = self.depth_image
        # show bounding box
        for obstacle in obstacle_region:
            bbox = obstacle[0]
            # print(bbox)
            # top, left, bottom, right = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            # cv2.rectangle(temp_image, (left, top), (right, bottom), (0, 255, 0), 2)
        # show path
        if path:
            for pixel in path:
                coords = pixel.coords
                # print(coords)
                cv2.circle(temp_image, coords, 10, (255,255,255), -1)
            plt.imshow(temp_image, cmap='gray')
            plt.axis('off')  # Turn off axis labels
            plt.savefig('./results/' + str(i) + '.jpg')