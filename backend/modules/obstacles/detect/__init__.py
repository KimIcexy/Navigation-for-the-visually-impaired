from ultralytics import YOLO
from threading import Thread
from ultralytics.utils.plotting import Annotator  # ultralytics.yolo.utils.plotting is deprecated
import cv2
import os

#os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:32"

# CHECK THIS LINK IN FUTURE
# https://stackoverflow.com/questions/10174211/how-to-make-an-always-relative-to-current-module-file-path

class ObjectDetection:
    """Detect objects in an image and return their bounding boxes and obstacle IDs.
    Atributes:
        model: the model used for object detection 
    """
    
    def __init__(self):
        self.model = self.get_model()
        
    def get_model(self):
        return YOLO('yolov8x.pt')
            
    def make_results_list (self, results):
        #https://docs.ultralytics.com/modes/predict/#inference-sources
        results_list = []
        for result in results:
            boxes = result.boxes
            result_list = []
            coords = result.boxes.xyxy.detach().cpu().numpy()
            obstacle_id = result.boxes.cls.detach().cpu().numpy()
            for x, y in zip (coords, obstacle_id):
                result_list.append ([x, self.model.names[int(y)]])
            results_list.append(result_list)
        return results_list

    def make_annotation (self, image_path, results, result_path):
        img = cv2.imread (image_path)
        for r in results:
            annotator = Annotator(img)
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]  # (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, self.model.names[int(c)])
        img = annotator.result()
        cv2.imwrite (result_path, img)

    def run(self, image_path, output_folder):
        results = []
        results = self.model(image_path)
        results_list = self.make_results_list(results)
        return results_list
        # print('Results list: ', results_list)
        
        # file_name = os.path.basename(image_path)
        # if not os.path.exists(output_folder):
        #     os.makedirs(output_folder)
        # result_path = os.path.join(output_folder, file_name)
        # self.make_annotation(image_path, results, result_path)
        # print('Complete saving result images at ' + output_folder)