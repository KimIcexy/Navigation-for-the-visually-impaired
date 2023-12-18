#import sys
#sys.path.append('../')
#from obstacles import ObjectDetection as OD
import ObjectDetection as OD
import cv2
import numpy as np
def nigger (videoPath, model, outputVideoPath, showVid = 0):
        tracker = cv2.TrackerCSRT_create()
        # Get the video file and read it
        video = cv2.VideoCapture(videoPath)
        ret, frame = video.read()
        # Resize the video for a more convinient view
        # Initialize video writer to save the results
        frame_height, frame_width = frame.shape[:2]
        frame = cv2.resize(frame, [frame_width//2, frame_height//2])
        frame_height, frame_width = frame.shape[:2]
        #output = cv2.VideoWriter(outputVideoPath, 
        #                         cv2.VideoWriter_fourcc(*'XVID'), 30.0, 
        #                         (frame_width//2, frame_height//2), True)
        output = cv2.VideoWriter(outputVideoPath, 
                                 cv2.VideoWriter_fourcc(*'XVID'), 30.0, 
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
                #print (frame.shape)
                frame = cv2.resize(frame, [frame_width, frame_height])
                if (count == 0):
                        result = model (frame)
                        #Temp, only tracking the first car occurence
                        #See https://docs.opencv.org/3.4/d8/d77/classcv_1_1MultiTracker.html
                        #    for multi-tracking
                        outputClassList = np.nonzero(result[0].boxes.data.numpy().astype (np.int32)[:][:,5]==2)[0]
                        if (len (outputClassList) != 0):
                                bbox = result[0].boxes.data.numpy().astype (np.int32)[outputClassList[0]][0:4]
                                ret = tracker.init(frame, bbox)
                                isTracked = 1
                        else:
                                bbox = result[0].boxes.data.numpy().astype (np.int32)[0][0:4]
                                ret = tracker.init(frame, bbox)
                                count = count - 1
                timer = cv2.getTickCount()
                #print (frame.shape,"___")
                #print (frame)
                ret, bbox = tracker.update(frame)
                count = (count + 1) % 60
                        
                fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
                if ret:
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
        nigger ('VideoData/0.mp4', model, 'VideoData/Result/0.avi')
        nigger ('VideoData/0.5.mp4', model, 'VideoData/Result/0.5.avi')
        nigger ('VideoData/1.5.mp4', model, 'VideoData/Result/1.5.avi')