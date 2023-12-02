import numpy as np
import cv2

class PathPlanning:
    """note
   + obs detect --> determine the area without obstacles --> select the destination
   + cost value --> directly use depth image or calculate the cost more??
   + determine the start: 
       ++ not in the area containing the obstacle
       ++ bottom of the image (maximum y ordinate)
   + determine temp goal (destination):
   + Algorithm to find the path from start to the destination
    """
    
    def __init__(self, depth_image, bounding_boxes):
        self.depth_image = depth_image
        self.bounding_boxes = bounding_boxes
    
    def show_bounding_boxes(self):
        # format: center coord: (bx, by), size (bw, bh) (normalized)
        temp_image = np.copy(self.depth_image)
        print('depth image shape: ', temp_image.shape)
        for bbox in self.bounding_boxes:
            x = int((float(bbox[0])-float(bbox[2])/2) *self.depth_image.shape[1]) # bx * width (n_columns)
            y = int((float(bbox[1])-float(bbox[3])/2) *self.depth_image.shape[0]) # by * height (n_rows)
            w = int(float(bbox[2])*self.depth_image.shape[1]) # bw * width
            h = int(float(bbox[3])*self.depth_image.shape[0]) # bh * height
            cv2.rectangle(temp_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        self.find_start_point(temp_image)
        cv2.imshow('Bounding boxes', temp_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
      
    def assign_costs(self):
        # use directly depth image (not sure !!)
        # check cost image: resize for fast check (30x30), not use origin depth image
        # print the check image
        pass
    
    def find_start_point(self, temp_image):
        # start point: mid bottom point in the image
        # calculate, mark point on the image to check
        radius = 10
        x = int(self.depth_image.shape[1] / 2)
        y = int(self.depth_image.shape[0]-radius)
        print('start: (', x, ', ', y, ')')
        cv2.circle(temp_image,(x,y), 10, (0,0,255), -1)
        return (x, y)
    
    def find_temp_goal(self):
        # calculate, mark point on the image to check
        # 1. not in obstacle area
        # 2. 
        # cost: càng xa vùng cản, cost càng nhỏ
        # lấy mẫu những pixel ko nằm trong vùng cản + có cost min
        # chọn ra dãy pixel liên tục dài nhất thỏa điều kiện
        # temp_goal: điểm thuộc dãy pixel trên và gần nhất với trung điểm của dãy
        
        pass
    
    def search_path(self):
        # use search algorithm from start to temp goal
        pass