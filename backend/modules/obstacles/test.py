import cv2
import os
from detect import ObjectDetection
from navigate.path_planning.floor_detect import FloorDetection

"""Preprocess: extract frames"""
# N_FRAMES = 1159
# print('N frames = ', N_FRAMES)

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

# video_path = './clip.mp4'
# extract_frames(video_path, output_folder)

"""Test object detection"""
# obj_detection = ObjectDetection()
output_folder = 'test_resources/frames'

frame_path = os.path.join(output_folder, str(1) + '.jpg')
# print('frame path: ', frame_path)
# obj_detection.run(frame_path, 'test_resources/results')
    
"""Test navigation"""
"""Test floor detect, merge later..."""
floor_detection = FloorDetection()
floor_detection.run(frame_path)