#import sys
#sys.path.append('../')
#from obstacles import ObjectDetection as OD
import ObjectDetection as OD
if __name__ == '__main__':
        model = OD.get_model()
        results = OD.model('testing_folder/bus.jpg')
