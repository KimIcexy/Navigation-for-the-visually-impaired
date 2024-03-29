import numpy as np
import cv2
import math
from matplotlib import pyplot as plt
import os

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
    
    def __init__(self, depth_image, obstacle_region, floor_region, old_path):
        self.depth_image = depth_image
        self.height = depth_image.shape[0]
        self.width = depth_image.shape[1]
        self.obstacle_region = obstacle_region
        self.walkable_map = self.create_walkable_map(obstacle_region, floor_region)
        self.planning_map = self.create_planning_map()
        point = self.find_start_point(old_path)
        print('find start point: ', point)
        if point == None:
            self.start = None
            self.goal = None
            return
        self.start = self.planning_map[point[1], point[0]]
        self.start.total_cost = 0
        self.start.cost = 0
        print('Start coords: ', self.start.coords)
        print('walkable: ', self.start.walkable)
        point = self.make_temp_goal()
        print('Temp goal: ', point)
        if point == self.start.coords or point == None:
            self.goal = None
            return
        self.goal = self.planning_map[point[1], point[0]]
        print('walkable: ', self.goal.walkable)
    
    def find_start_point(self, old_path):
        path_len = len(old_path)
        # print('len old path: ', path_len)
        if path_len == 0:
            # start point: mid bottom point in the image
            x = int(self.width / 2)
            y = int(self.height - 1)
            return (x, y)
        else:
            # reversed_path
            for i_reversed in range (path_len -1, -1, -1):
                coords = old_path[i_reversed]
                # print('coords reversed: ', coords)
                node = self.planning_map[coords[1], coords[0]]
                if node.walkable:
                    if i_reversed != path_len-1: # old goal is walkable
                        # print('i_reversed: ', i_reversed)
                        self.update_old_path(old_path, i_reversed)
                        # print('update len: ', len(old_path))
                    return node.coords
            return None
            
    def update_old_path(self, old_path, new_end_idx):
        # print(old_path[new_end_idx+1:])
        old_path[:] = old_path[:new_end_idx+1]
        
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
        center = int(len(path)/2 -1)
        return path[center]
    
    def create_walkable_map(self, obstacle_region, floor_region):
        bbox_margin = 10
        walkable_map = np.zeros((self.height, self.width), dtype=bool)
        
        for bbox in floor_region:
            top, left, bottom, right = bbox
            top, left, bottom, right = max(0, top - bbox_margin), \
                                    max(0, left - bbox_margin), \
                                    min(bottom + bbox_margin, self.height - 1), \
                                    min(right + bbox_margin, self.width - 1)
            walkable_map[top:bottom + 1, left:right + 1] = True
        
        for obstacle in obstacle_region:
            bbox = obstacle[0]
            left, top, right, bottom = bbox
            left, top, right, bottom = int(max(0, left - bbox_margin)), \
                                    int(max(0, top - bbox_margin)), \
                                    int(min(right + bbox_margin, self.width - 1)), \
                                    int(min(bottom + bbox_margin, self.height - 1))
            walkable_map[top:bottom + 1, left:right + 1] = False
        
        return walkable_map

    def create_planning_map(self):
        planning_map = np.array([
            [PixelNode(coords=(x, y),
                       depth=self.depth_image[y, x],
                       walkable=self.walkable_map[y, x],
                       cost=255 - self.depth_image[y, x])
             for x in range(self.width)]
            for y in range(self.height)
        ])
        return planning_map
    
    def heuristic(self, pixel):
        goal_coords = self.goal.coords
        pixel_coords = pixel.coords
        return np.sqrt((goal_coords[0] - pixel_coords[0]) ** 2 + (goal_coords[1] - pixel_coords[1]) ** 2)
    
    def get_neighbors(self, current_node):
        if current_node.neighbors is None:
            x, y = current_node.coords
            neighbors_row = self.planning_map[y, max(x-1, 0):min(x+2, self.width-1)].flatten()
            neighbors_col = self.planning_map[max(y-1, 0):min(y+1, self.height-1), x].flatten()

            new_neighbors = np.concatenate((neighbors_col, neighbors_row))
            new_neighbors_list = [neighbor for neighbor in new_neighbors if neighbor.coords != current_node.coords and neighbor.walkable]
            current_node.neighbors = np.array(new_neighbors_list)        
                
    def search_path(self):
        # use A* search algorithm from start to goal
        open_set = [self.start]
        closed_set = set()
        
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
                    path = [current_node.coords]
                    while pre_node:
                        path.insert(0, pre_node.coords)
                        pre_node = pre_node.pre_node
                    return path
                
                # pop the current_node out of the open_set:
                open_set.remove(current_node)
                
                # assign neighbors for current_node:
                self.get_neighbors(current_node)

                # traverse all neighbors of current_node:
                # print('current_node: ', current_node.coords)
                for neighbor in current_node.neighbors:
                    # print('current total cost: ', current_node.total_cost)
                    # print('neighbor total cost: ', neighbor.total_cost)
                    # print('neighbor cost: ', neighbor.cost)
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

    def path_to_direction (self, optimized_path):
        direction = ["Right", "Left"]
        output_direction = ["Straight"]
        output_distance = []
        last_checkpoint = 0
        vec_before = (0,-1)
        for a in range (0, len(optimized_path)-1):
                #print (optimized_path[a])
                vec_after = ((optimized_path[a+1][0] - optimized_path[a][0]), (optimized_path[a+1][1] - optimized_path[a][1]))
                if (vec_before == vec_after):
                        continue
                if (vec_before[0] == 0):
                        if (vec_before[1] == 1):
                                output_direction.append (direction[vec_after[0] == 1])
                        else: #== -1
                                output_direction.append (direction[vec_after[0] == -1])
                else:
                        if (vec_before[0] == 1):
                                output_direction.append (direction[vec_after[1] == -1])
                        else: #== -1
                                output_direction.append (direction[vec_after[1] == 1])
                output_direction.append ("Straight")
                output_distance.append (a - last_checkpoint)
                last_checkpoint = a
                vec_before = vec_after
        output_distance.append (len(optimized_path)-1 - last_checkpoint)
        try:
            if output_distance [0] <= 5:
                output_distance.pop(0)
                output_direction.pop(0)
        except:
            pass
        return output_direction, output_distance
    
    def test_path_to_direction(self, optimized_path, no_frame):
        output_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_file_path = os.path.join(os.path.dirname(output_file_path), 'results', 'direction', f'{no_frame}.txt')
        direction = ["Right", "Left"]
        output_direction = ["Straight"]
        output_distance = []
        last_checkpoint = 0
        vec_before = (0,-1)

        with open(output_file_path, 'w') as output_file:
            for a in range (0, len(optimized_path)-1):
                #print (optimized_path[a])
                vec_after = ((optimized_path[a+1][0] - optimized_path[a][0]), (optimized_path[a+1][1] - optimized_path[a][1]))
                if (vec_before == vec_after):
                        continue
                if (vec_before[0] == 0):
                        if (vec_before[1] == 1):
                                output_direction.append (direction[vec_after[0] == 1])
                        else: #== -1
                                output_direction.append (direction[vec_after[0] == -1])
                else:
                        if (vec_before[0] == 1):
                                output_direction.append (direction[vec_after[1] == -1])
                        else: #== -1
                                output_direction.append (direction[vec_after[1] == 1])
                output_direction.append ("Straight")
                output_distance.append (a - last_checkpoint)
                last_checkpoint = a
                vec_before = vec_after
            output_distance.append (len(optimized_path)-1 - last_checkpoint)
            try:
                if output_distance [0] <= 5:
                    output_distance.pop(0)
                    output_direction.pop(0)
            except:
                pass
            print(output_direction, file=output_file)
            print(output_distance, file=output_file)
        return output_direction, output_distance
  
    def optimize_path (self, raw_path, segment_len = 15, max_distance = 20):
        def append_path (out_array, vec_x, vec_y):
            if (abs(vec_x) > abs(vec_y)):
                if (vec_y != 0):
                    last_y = out_array[len(out_array)-1][1]
                    direction = int(vec_y/abs(vec_y))
                    for y in range (last_y + direction, last_y + vec_y + direction, direction):
                        out_array.append ((out_array[len(out_array)-1][0], y))
                if (vec_x != 0):
                    last_x = out_array[len(out_array)-1][0]
                    direction = int(vec_x/abs(vec_x))
                    for x in range (last_x + direction, last_x + vec_x + direction, direction):
                        out_array.append ((x, out_array[len(out_array)-1][1]))
            else:
                if (vec_x != 0):
                    last_x = out_array[len(out_array)-1][0]
                    direction = int(vec_x/abs(vec_x))
                    for x in range (last_x + direction, last_x + vec_x + direction, direction):
                        out_array.append ((x, out_array[len(out_array)-1][1]))
                if (vec_y != 0):
                    last_y = out_array[len(out_array)-1][1]
                    direction = int(vec_y/abs(vec_y))
                    for y in range (last_y + direction, last_y + vec_y + direction, direction):
                        out_array.append ((out_array[len(out_array)-1][0], y))
            return out_array
        
        #Input: List of tuple (example: [(6969, 50),...])
        #Output: Optimized list of tuple
        #segment_len cang cao thi cang don gian hoa duong di
        a = 0
        segment_len = segment_len * segment_len
        out_array = [[raw_path[0][0],raw_path[0][1]]]
        #Cumulative of vector that has not been used in path
        cum_vec_x = 0
        cum_vec_y = 0
        while (a < len(raw_path)):
            segment_end = min (a + segment_len, len(raw_path)-1)
            vec_x = raw_path [segment_end][0] - raw_path[a][0]
            vec_y = raw_path [segment_end][1] - raw_path[a][1]
            if (cum_vec_x == 0) and (cum_vec_y == 0):
                if abs(vec_x) <= abs (vec_y):
                    out_array = append_path (out_array, 0, vec_y)
                    cum_vec_x = vec_x
                else:
                    out_array = append_path (out_array, vec_x, 0)
                    cum_vec_y = vec_y
                
            elif (cum_vec_x == 0) and (cum_vec_y!=0):
                out_array = append_path (out_array, vec_x, 0)
                cum_vec_y = cum_vec_y + vec_y
                if abs(cum_vec_y) >= max_distance:
                    out_array = append_path (out_array, 0, cum_vec_y)
                    cum_vec_y = 0                    
            elif (cum_vec_y == 0) and (cum_vec_x!=0):
                out_array = append_path (out_array, 0, vec_y)
                cum_vec_x = cum_vec_x + vec_x
                if abs(cum_vec_x) >= max_distance:
                    out_array = append_path (out_array, cum_vec_x, 0)
                    cum_vec_x = 0
            #out_array = append_path (out_array, vec_x, vec_y)
            a = a + segment_len
        out_array = append_path (out_array, cum_vec_x, cum_vec_y)
        return out_array
    
    def show_result(self, origin_image, path, no_frame, optimized=True):
        rgb_image = origin_image.copy()
        # # show bounding box
        # for obstacle in obstacle_region:
        #     bbox = obstacle[0]
        #     # print(bbox)
        #     # top, left, bottom, right = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        #     # cv2.rectangle(temp_image, (left, top), (right, bottom), (0, 255, 0), 2)
        
        # show path
        if path:
            for pixel in path:
                # coords = pixel.coords
                # print(coords)
                cv2.circle(rgb_image, pixel, 10, (0,255,0), -1)
            plt.imshow(rgb_image, cmap='gray')
            plt.axis('off')  # Turn off axis labels
            result_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            if optimized:
                result_path = os.path.join(os.path.dirname(result_path), 'results', 'path', f'{no_frame}.jpg')
            else:
                result_path = os.path.join(os.path.dirname(result_path), 'results', 'path', f'{no_frame}_raw.jpg')

            print('result path: ', result_path)
            plt.savefig(result_path)

    def get_results(self, path, directions):
        results = {}

        # obstacle results have type: [[top, left, bottom, right], class_name]
        obstacle_results = []
        for obstacle in self.obstacle_region:
            bbox = obstacle[0]
            top, left, bottom, right = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
            class_name = obstacle[1]
            obstacle_results.append([[top, left, bottom, right], class_name])
        results['obstacles'] = obstacle_results
        results['path'] = path
        results['directions'] = directions

        return [results]

