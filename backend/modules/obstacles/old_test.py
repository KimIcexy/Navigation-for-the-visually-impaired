import cv2
import os
# import matplotlib.pyplot as plt

# from detect import ObjectDetection
# from detect.floor_detect import FloorDetection
# from navigate.path_planning import PathPlanning
# from navigate.rgb2depth import MakeDepthImage

"""Preprocess: extract frames"""
# N_FRAMES = 1159
# print('N frames = ', N_FRAMES)

def extract_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) # 1834 frames
    for frame_number in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break
        filename = f"{frame_number + 1}.jpg"
        filepath = os.path.join(output_folder, filename)
        cv2.imwrite(filepath, frame)
    cap.release()
    print(f"{total_frames} frames have been extracted and saved to {output_folder}.")

video_path = 'test_resources/video.mp4'
output_folder = 'test_resources/frames'
extract_frames(video_path, output_folder)

# """Test object detection"""
# obj_detection = ObjectDetection()
# output_folder = 'test_resources/frames'

# frame_path = os.path.join(output_folder, str(16) + '.jpg')
# print('frame path: ', frame_path)
# print('Obstacle detection...')
# obstacle_region = obj_detection.run(frame_path)
# # print('Obstacles: ', obstacle_region[0])

# """Test navigation"""
# print('Floor detection...')
# floor_detection = FloorDetection()
# floor_region = floor_detection.run(frame_path)

# """Test depth converter"""
# # # depth_converter = MakeDepthImage()
# # # depth_image = depth_converter.run(frame_path)
# print('rgb >> depth')
# result_path = './navigate/rgb2depth/depth_image.png'
# origin_size = (1080, 1920)
# depth_image = cv2.imread(result_path, cv2.IMREAD_GRAYSCALE)
# depth_image = cv2.resize(depth_image, origin_size)
# # # print(depth_image.shape)
# # # plt.imshow(depth_image, cmap='gray')
# # # plt.axis('off')  # Turn off axis labels
# # # plt.show()

# """Test path planning"""
# print('Path planning...')
# path_planning = PathPlanning(depth_image, obstacle_region[0], floor_region)
# path = path_planning.search_path()
# # print('Path: ', path)
# path_planning.show_result(obstacle_region, path, 7)