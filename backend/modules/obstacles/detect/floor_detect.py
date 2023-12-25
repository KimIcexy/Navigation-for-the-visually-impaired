from roboflow import Roboflow
import os

class FloorDetection:
    def __init__(self):
        rf = Roboflow(api_key="rhADRHQ1t9je2cWjdWgW")
        project = rf.workspace().project("floor-detection-btxc3")
        self.model = project.version(2).model
    
    def predict(self, image_path):
        return self.model.predict(image_path, confidence=40, overlap=30)
    
    def make_results_list (self, results):
        results_list = []
        for result in results:
            top = result['y'] - 0.5 * result['height']
            left = result['x'] - 0.5 * result['width']
            bottom = result['y'] + 0.5 * result['height']
            right = result['x'] + 0.5 * result['width']
            results_list.append([int(top), int(left), int(bottom), int(right)])
        # print('Result list: ', results_list)
        return results_list

    def make_annotations(self, results, no_frame):
        result_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        result_path = os.path.join(result_path, 'results', 'floor', f'{no_frame}.jpg')
        print('floor path: ', result_path)
        results.save(result_path)
        
    def run(self, image_path, no_frame):
        results = self.predict(image_path)
        # print('floor region: ', results)
        self.make_annotations(results, no_frame)
        return self.make_results_list(results)
        