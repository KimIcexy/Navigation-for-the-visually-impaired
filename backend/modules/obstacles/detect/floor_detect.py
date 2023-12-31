from roboflow import Roboflow
import os
import cv2

class FloorDetection:
    def __init__(self):
        rf = Roboflow(api_key="rhADRHQ1t9je2cWjdWgW")
        project = rf.workspace().project("floor-detection-btxc3")
        self.model = project.version(2).model
    
    def predict(self, image_path):
        return self.model.predict(image_path, confidence=40, overlap=30)
    
    def make_results_list (self, results):
        results_list = []
        # remove the second floor detection
        for result in results:
            top = result['y'] - 0.5 * result['height']
            left = result['x'] - 0.5 * result['width']
            bottom = result['y'] + 0.5 * result['height']
            right = result['x'] + 0.5 * result['width']
            results_list.append([int(top), int(left), int(bottom), int(right)])
        # print('Result list: ', results_list)
        
        
        # Just get the only one floor region which has max bottom coordinate
        if len(results) > 1:
            final_result = results_list[0]
            for result in results_list[1:]:
                if result[2] > final_result[2]:
                    final_result = result               
            results_list = [final_result]
        return results_list

    def make_annotations(self, results, image, no_frame):
        temp_image = image.copy()
        result_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        result_path = os.path.join(result_path, 'results', 'floor', f'{no_frame}.jpg')
        # print('floor path: ', result_path)
        cv2.rectangle(temp_image, (results[0][1], results[0][0]), (results[0][3], results[0][2]), (0, 255, 0), 2)
        cv2.imwrite(result_path, temp_image)
        
    def test(self, image, no_frame):
        results = self.make_results_list(self.predict(image))
        # print('floor region: ', results)
        self.make_annotations(results, image, no_frame)
        return results
    
    def run(self, image):
        return self.make_results_list(self.predict(image))
        