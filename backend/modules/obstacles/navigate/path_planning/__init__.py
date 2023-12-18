import numpy as np
import cv2
import math

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
 
    Atributes:
        depth_image: depth image
        bounding_boxes: obstacle bounding boxes
        walkable_map: map showing walkable or non-walkable pixel
        planning_map: map of PixelNode which used to path planning
        start: PixelNode that begin to path planning
        goal: PixelNode that the path planning want to reach        
    """  
    
    def __init__(self, depth_image, bounding_boxes):
        self.depth_image = depth_image
        self.bounding_boxes = self.read_bounding_boxes(bounding_boxes)
        self.walkable_map = self.create_walkable_map()
        self.planning_map = self.create_planning_map()
        point = self.find_start_point()
        self.start = self.planning_map[point[1], point[0]]
        self.start.total_cost = 0
        self.start.cost = 0
        point = self.hard_code_temp_goal()
        self.goal = self.planning_map[point[1], point[0]]
        
    def read_bounding_boxes(self, bounding_boxes):
        # format: center coord: (bx, by), size (bw, bh) (normalized),
        # may need to change later based on the output format from the module 3 !!!
        bboxes = []
        for bbox in bounding_boxes:
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
    
    def hard_code_temp_goal(self):
        x = int(0.43 * self.depth_image.shape[1])
        # x = int(self.depth_image.shape[1] / 2)
        y = int(0.85 * self.depth_image.shape[0])
        return (x, y)
    
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
    
    def create_walkable_map(self):
        walkable_map = np.ones((self.depth_image.shape[0], self.depth_image.shape[1]), dtype=bool)
        bbox_margin = 10
        for bbox in self.bounding_boxes:
            bx, by, bw, bh = bbox[0], bbox[1], bbox[2], bbox[3]
            walkable_map[int(by)-bbox_margin:int(by+bh)+bbox_margin, int(bx)-bbox_margin:int(bx+bw)+bbox_margin] = False
        return walkable_map        
    
    def heuristic(self, pixel):
        goal_coords = self.goal.coords
        pixel_coords = pixel.coords
        return np.sqrt((goal_coords[0] - pixel_coords[0]) ** 2 + (goal_coords[1] - pixel_coords[1]) ** 2)

    def get_neighbors(self, current_node, neighbor_type='4'):
        x, y = current_node.coords
        if (neighbor_type=='8'):
            neighbors = self.planning_map[max(y-1, 0):min(y+2, self.depth_image.shape[0]), \
                                        max(x-1, 0):min(x+2, self.depth_image.shape[1])]
            neighbors = neighbors.flatten()
            for i in range(neighbors.shape[0]):
                if neighbors[i].coords == current_node.coords:
                    current_node.neighbors = np.delete(neighbors, i)
                    return
                
        # neighbor_type='4':
        neighbors_row = self.planning_map[y, max(x-1, 0):min(x+2, self.depth_image.shape[1])].flatten()
        neighbors_col = self.planning_map[max(y-1, 0):min(y+2, self.depth_image.shape[0]), x].flatten()

        new_neighbors = np.concatenate((neighbors_col, neighbors_row))
        new_neighbors_list = []
        for neighbor in new_neighbors:
            if neighbor.coords != current_node.coords:
                new_neighbors_list.append(neighbor)
        current_node.neighbors = np.array(new_neighbors_list)
        
    def search_path(self):
        # use A* search algorithm from start to goal
        open_set = [self.start]
        closed_set = set()
        print('start node: ', self.start.coords)
        print('end node: ', self.goal.coords)
        
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
    
    def show_result(self, path):
        temp_image = self.depth_image
        # show bounding box
        for (x, y, w, h) in self.bounding_boxes:
            cv2.rectangle(temp_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # show path
        if path:
            for pixel in path:
                coords = pixel.coords
                # print(coords)
                cv2.circle(temp_image, coords, 10, (255,255,255), -1)
        cv2.imshow('Bounding boxes', temp_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
