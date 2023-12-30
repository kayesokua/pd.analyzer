from flask import current_app

import os
import cv2
import pandas as pd
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2

from .pose_add_features import *
from .pose_classifier import *
from .data_visualization import *
from .converter_gif import *

def draw_landmarks_on_image(rgb_image, detection_result):
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)
    
    for idx, pose_landmarks in enumerate(pose_landmarks_list):
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        pose_landmarks_proto.landmark.extend([
            landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in pose_landmarks
        ])

        solutions.drawing_utils.draw_landmarks(
            annotated_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style())

    return annotated_image

def create_pose_landmark_dictionary(new_frames_path):
    model_path = os.path.join(current_app.root_path, 'models', 'ml', 'pose_landmarker.task')
    print(model_path)
    
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.PoseLandmarkerOptions(base_options=base_options,output_segmentation_masks=True)
    landmarker = vision.PoseLandmarker.create_from_options(options)

    filenames = [os.path.join(new_frames_path, f) for f in os.listdir(new_frames_path) if f.endswith(".png")]
    filenames.sort()
    pose_data = []
    error = 0

    for image_file_path in filenames:
        try:
            image_rgb = cv2.imread(image_file_path, cv2.IMREAD_COLOR)
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_bgr)
            
            detection_result = landmarker.detect(mp_image)
            
            if detection_result:
                annotated_image = draw_landmarks_on_image(image_bgr, detection_result)
                annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                annotated_image_path = os.path.join(new_frames_path, 'annotated_' + os.path.basename(image_file_path))
                cv2.imwrite(annotated_image_path, annotated_image_rgb)
                
                image_basename = os.path.basename(image_file_path).split('.')[0]
                
                plot_filepath = os.path.join(new_frames_path, 'plot')
                plot_filename = os.path.join(plot_filepath, f'{image_basename}.png')
            
                for pose_landmarks in detection_result.pose_landmarks:
                    pose_info = {
                        'filename': image_file_path,
                        'plot_filename': plot_filename,
                        'annotated_filename':annotated_image_path}
                    
                    for idx,landmark in enumerate(pose_landmarks):
                        idx_str = str(idx).zfill(2)
                        pose_info[f'landmark_{idx_str}_x'] = landmark.x
                        pose_info[f'landmark_{idx_str}_y'] = landmark.y
                        pose_info[f'landmark_{idx_str}_z'] = landmark.z
                        pose_info[f'landmark_{idx_str}_v'] = landmark.visibility
                    pose_data.append(pose_info)
                
            else:
                print(f"No pose detected for {image_file_path}")
                error += 1
       
        except Exception as e:
            print(f"Error processing {image_file_path}: {e}")

    pose_df = pd.DataFrame(pose_data)
    
    x_columns = sorted([col for col in pose_df.columns if col.endswith('_x')])
    y_columns = sorted([col for col in pose_df.columns if col.endswith('_y')])
    
    pose_features1_df = pose_df.apply(lambda row: condense_pole_dictionary(row, x_columns, y_columns), axis=1)
    pose_features1_df['orientation'] = pose_features1_df.apply(classify_row_orientation, axis=1)
    pose_features2_df = compute_connected_joints_angles(pose_features1_df)
    pose_features3_df = calculate_pose_angle_difference(pose_features2_df)
    
    pose_features3_df.to_csv(f'{new_frames_path}/results.csv',index=False)

    return pose_features3_df