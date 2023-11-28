import cv2

from __init__ import PathPlanning

# Read the image
test_image_path = './result.png'
depth_image = cv2.imread(test_image_path)

# Read the bounding boxes
result_string = """
class,confidence,bx,by,bw,bh
chair,1.00,0.23,0.68,0.04,0.15
chair,1.00,0.30,0.67,0.03,0.14
chair,1.00,0.28,0.67,0.04,0.15
chair,0.98,0.25,0.68,0.04,0.15
sofa,0.89,0.76,0.83,0.17,0.26
pottedplant,0.95,0.88,0.84,0.19,0.29
pottedplant,1.00,0.53,0.69,0.06,0.12
bed,0.63,0.59,0.67,0.24,0.14
tvmonitor,1.00,0.34,0.52,0.06,0.10
microwave,1.00,0.07,0.49,0.13,0.11
refrigerator,1.00,0.11,0.76,0.22,0.44
"""
lines = result_string.strip().split('\n')
bounding_boxes = [line.split(',') for line in lines[1:]]
print('bb string: ', bounding_boxes)
bounding_boxes = [bbox[2:] for bbox in bounding_boxes] # remove class,confidence
print(bbox for bbox in bounding_boxes)


# Init path planning
path_planning = PathPlanning(depth_image, bounding_boxes)
path_planning.show_bounding_boxes()
# path_planning.assign_costs()
# path_planning.find_start_point()
# path_planning.find_temp_goal()
# path_planning.search_path()