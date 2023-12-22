from roboflow import Roboflow

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

    def make_annotations(self, results):
        results.save("prediction.jpg")
        
    def run(self, image_path):
        results = self.predict(image_path)
        # print('floor region: ', results)
        # self.make_annotations(results)
        return self.make_results_list(results)
        