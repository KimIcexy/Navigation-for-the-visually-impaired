#import sys
#sys.path.append('../')
#from obstacles import ObjectDetection as OD
import ObjectDetection as OD
import backend.modules.obstacles.detect.utils as UT
import cv2
import numpy as np
import time
classNum,_ = UT.readClass('COCO-Classes_Filtered.txt')
print (classNum)
try:
        classNum.remove (0)
except:
        pass
print (classNum)
def nigger (videoPath, model, outputVideoPath, showVid = 0):
        video = cv2.VideoCapture(videoPath)
        ret, frame = video.read()
        frame_height, frame_width = frame.shape[:2]
        frame = cv2.resize(frame, [frame_width//2, frame_height//2])
        frame_height, frame_width = frame.shape[:2]
        output = cv2.VideoWriter(outputVideoPath, 
                                 cv2.VideoWriter_fourcc(*'XVID'), 60.0, 
                                 (frame_width, frame_height), True)
        if not ret:
            print('cannot read the video')
            return
        # Start tracking
        count = 0
        isTracked = 0
        while True:
                ret, frame = video.read()
                if not ret:
                        print('Stopping')
                        break
                frame = cv2.resize(frame, [frame_width, frame_height])
                if (count == 0):
                        result = model (frame)
                        #Temp, only tracking the first car occurence
                        #See https://docs.opencv.org/3.4/d8/d77/classcv_1_1MultiTracker.html
                        #    for multi-tracking
                        multiTracker = cv2.legacy.MultiTracker_create()
                        #y,x) 
                        #outputClassList = np.nonzero(result[0].boxes.data.cpu().numpy().astype (np.int32)[:][:,5]==2)[0]
                        outputClassList = np.nonzero(np.in1d(result[0].boxes.data.cpu().numpy().astype (np.int32)[:][:,5], classNum))[0]
                        #print (outputClassList)
                        #print (result[0].boxes.data.cpu().numpy().astype (np.int32)[:][:,5])
                        if (len (outputClassList) != 0):
                                for a in outputClassList:
                                        tracker = cv2.legacy.TrackerMedianFlow_create()
                                        bbox = result[0].boxes.data.cpu().numpy().astype (np.int32)[a][0:4]
                                        bbox[2] = bbox[2] - bbox[0]
                                        bbox[3] = bbox[3] - bbox[1]
                                        #ret = tracker.init(frame, bbox)
                                        multiTracker.add (tracker, frame, bbox)
                                bboxs = multiTracker.getObjects()
                                isTracked = 1
                        else:
                                #bbox = result[0].boxes.data.cpu().numpy().astype (np.int32)[0][0:4]
                                #ret = tracker.init(frame, bbox)
                                #tracker = cv2.legacy.TrackerCSRT_create()
                                #multiTracker.add (tracker, frame, bbox)
                                count = count - 1
                timer = cv2.getTickCount()
                #print (frame.shape,"___")
                #print (frame)
                #start = time.time()
                ret, bbox = multiTracker.update(frame)
                #print('Tracking time taken (second): ',time.time() - start)
                try:
                        #print (len (multiTracker.getObjects()))
                        bboxs = multiTracker.getObjects()
                        #print ("Tracking bbox: ", bboxs)
                except Exception as e:
                        print ("Exception: ")
                        print (e)
                        pass
                count = (count + 1) % 30
                        
                fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
                if ret:
                        for bbox in bboxs:
                                p1 = (int(bbox[0]), int(bbox[1]))
                                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                                if (isTracked == 0):
                                        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
                                else:
                                        cv2.rectangle(frame, p1, p2, (0,255,0), 3, 1)
                        isTracked = 0
                else:
                        cv2.putText(frame, "Tracking failure detected", (100,80), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
                cv2.putText(frame, "CSRT Tracker", (100,20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
                cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
                output.write(frame)
                if (showVid == 1):
                        cv2.imshow("Tracking", frame)
                        k = cv2.waitKey(1) & 0xff
                        if k == 27 : break
                
        video.release()
        output.release()
        cv2.destroyAllWindows()
        return 0

if __name__ == '__main__':
        model = OD.get_model()
        results = model('testing_folder/bus.jpg')
        while True:
                nigger ('VideoData/1.mp4', model, 'VideoData/Result/1.avi',1)
                nigger ('VideoData/0.mp4', model, 'VideoData/Result/0.avi',1)
                nigger ('VideoData/0.5.mp4', model, 'VideoData/Result/0.5.avi',1)
                nigger ('VideoData/1.5.mp4', model, 'VideoData/Result/1.5.avi',1)
