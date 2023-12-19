import cv2
import os
from detect import ObjectDetection

N_FRAMES = 1159
print('N frames = ', N_FRAMES)
# def extract_frames(video_path, output_folder):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     cap = cv2.VideoCapture(video_path)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # 1159 frames
#     for frame_number in range(total_frames):
#         ret, frame = cap.read()
#         if not ret:
#             break
#         filename = f"{frame_number + 1}.jpg"
#         filepath = os.path.join(output_folder, filename)
#         cv2.imwrite(filepath, frame)
#     cap.release()
#     print(f"{total_frames} frames have been extracted and saved to {output_folder}.")

obj_detection = ObjectDetection()
output_folder = 'test_resources/frames'
# video_path = './clip.mp4'
# extract_frames(video_path, output_folder)
frame_path = os.path.join(output_folder, str(1158) + '.jpg')
print('frame path: ', frame_path)
obj_detection.run(frame_path, 'test_resources/results')
    
# for i in range(0, N_FRAMES, 16):
#     frame_path = os.path.join(output_folder, str(i+1) + '.jpg')
#     ObjectDetection.run(frame_path, './results')