from ultralytics import YOLO

from threading import Thread
from ultralytics.utils.plotting import Annotator  # ultralytics.yolo.utils.plotting is deprecated
import cv2
import os
#os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:32"

# CHECK THIS LINK IN FUTURE
# https://stackoverflow.com/questions/10174211/how-to-make-an-always-relative-to-current-module-file-path


n_epochs = 20
batch_size = 32
workers = 3
selected_class_list = [0, 5]
def get_model():
        return YOLO('yolov8l.pt')
def model_train ():
        # Load a pretrained YOLO model (recommended for training)
        model = get_model()
        results = model.train(data='./coco_D_drive.yaml', epochs=n_epochs,
                              workers=workers, batch=batch_size)
        # Evaluate the model's performance on the validation set
        results = model.val()
def predict_img (model, url):
        #https://docs.ultralytics.com/modes/predict/#inference-sources
        results = model (url)
        results_list = []
        for result in results:
                boxes = result.boxes  # Boxes object for bbox outputs
                masks = result.masks  # Masks object for segmentation masks outputs
                keypoints = result.keypoints  # Keypoints object for pose outputs
                probs = result.probs  # Probs object for classification outputs
                result_list = []
                toa_do = result.boxes.xyxy.detach().cpu().numpy()
                ma_vat_the = result.boxes.cls.detach().cpu().numpy()
                for x, y in zip (toa_do, ma_vat_the):
                        result_list.append ([x, y])
                results_list.append (result_list)
        return results_list
def make_annotation (imgPath, results, savingImgPath = './temp/results.png'):
        img = cv2.imread (imgPath)
        for r in results:
                annotator = Annotator(img)
                boxes = r.boxes
                for box in boxes:
                    b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
                    c = box.cls
                    annotator.box_label(b, model.names[int(c)])
        img = annotator.result()
        cv2.imwrite (savingImgPath, img)

if __name__ == '__main__':
        model = get_model()
        results = model('./testing_folder/bus.jpg')
        make_annotation('./testing_folder/bus.jpg', results, 'testing_folder/bus_result.jpg')
        """
        <class 'tuple'>
        bbox
        (33, 253, 764, 469)"""

        pass
        #cv2.imshow('YOLO V8 Detection', img)     
        #if cv2.waitKey(1) & 0xFF == ord(' '):
        #        cv2.destroyAllWindows()
                
        # Perform object detection on an image using the model
        #results = model('https://ultralytics.com/images/bus.jpg')
        #result = predict_img (model, 'test.jpg')
        #result = predict_img (model, 'https://ultralytics.com/images/bus.jpg')
        #result = predict_img (model, 'https://ultralytics.com/images/bus.jpg')
        #print (result[0].boxes.xyxy.detach().cpu().numpy())
        # Export the model to ONNX format
        #success = model.export(format='onnx')


# Create a new YOLO model from scratch
#model = YOLO('yolov8l.yaml')
