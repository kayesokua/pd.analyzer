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
import logging


from .pose_add_features import *
from .pose_classifier import *

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

def create_pose_landmark_dictionary(new_frames_path, model_path):
    annotated_dir = os.path.join(new_frames_path,'annotated')
    os.makedirs(annotated_dir, exist_ok=True)
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.PoseLandmarkerOptions(base_options=base_options,output_segmentation_masks=True)
    landmarker = vision.PoseLandmarker.create_from_options(options)
    logging.basicConfig(level=logging.DEBUG)
    
    
    try:
        filenames = [os.path.join(new_frames_path, f) for f in os.listdir(new_frames_path) if f.endswith(".png")]
        filenames.sort()
        
        pose_data = []
        pose_world_data = []
        
        error = 0

        for image_file_path in filenames:
            try:
                image_rgb = cv2.imread(image_file_path, cv2.IMREAD_COLOR)
                image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_bgr)
                
                detection_result = landmarker.detect(mp_image)
                
                if detection_result:
                    annotated_image = draw_landmarks_on_image(image_bgr, detection_result)
                    width, height = int(annotated_image.shape[1] * 0.4), int(annotated_image.shape[0] * 0.4)
                    resized_image = cv2.resize(annotated_image, (width, height), interpolation=cv2.INTER_AREA)
                    annotated_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
                    annotated_image_path = os.path.join(annotated_dir,os.path.basename(image_file_path))
                    cv2.imwrite(annotated_image_path, annotated_image_rgb)
                    frame_path = os.path.basename(image_file_path)
                                    
                    for pose_landmarks in detection_result.pose_landmarks:
                        pose_info = {'filepath_abs': image_file_path,
                                     'frame_name': frame_path[:-4]}
                        
                        for idx,landmark in enumerate(pose_landmarks):
                            idx_str = str(idx).zfill(2)
                            pose_info[f'landmark_{idx_str}_x'] = landmark.x
                            pose_info[f'landmark_{idx_str}_y'] = landmark.y
                            pose_info[f'landmark_{idx_str}_z'] = landmark.z
                            pose_info[f'landmark_{idx_str}_v'] = landmark.visibility
                        pose_data.append(pose_info)
                        
                    for pose_world_landmarks in detection_result.pose_world_landmarks:
                        pose_info = {'filepath_abs': image_file_path,
                                     'frame_name': frame_path[:-4]}
                        
                        for idx,landmark in enumerate(pose_world_landmarks):
                            idx_str = str(idx).zfill(2)
                            pose_info[f'landmark_{idx_str}_x'] = landmark.x
                            pose_info[f'landmark_{idx_str}_y'] = landmark.y
                            pose_info[f'landmark_{idx_str}_z'] = landmark.z
                            pose_info[f'landmark_{idx_str}_v'] = landmark.visibility
                        pose_world_data.append(pose_info)
                    
                else:
                    print(f"No pose detected for {image_file_path}")
                    error += 1
        
            except Exception as e:
                print(f"Error processing {image_file_path}: {e}")

        pose_norm_df = pd.DataFrame(pose_data)
        pose_world_df = pd.DataFrame(pose_world_data)

        # Transforming pose landmark data...
        x_columns = sorted([col for col in pose_norm_df.columns if col.endswith('_x')])
        y_columns = sorted([col for col in pose_norm_df.columns if col.endswith('_y')])
        z_columns = sorted([col for col in pose_norm_df.columns if col.endswith('_z')])
        
        # Spatial Orientation Feature
        pose_2d_df = pose_norm_df.apply(lambda row: condense_pole_dictionary(row, x_columns, y_columns), axis=1)
        pose_2d_df['orientation'] = pose_2d_df.apply(classify_row_orientation, axis=1)

        # Pose Angles Feature
        pose_2d_features_df = compute_connected_joints_angles(pose_2d_df)

        # Rate of Change Features
        pose_2d_features2_df = calculate_pose_angle_difference(pose_2d_features_df)

        # Save Results
        pose_2d_features2_df.to_csv(f'{new_frames_path}/pose_norm_data.csv',index=False)

        # Spatial Orientation Feature
        pose_3d_df = pose_world_df.apply(lambda row: condense_pole_dictionary_3d(row, x_columns, y_columns, z_columns), axis=1)
        pose_3d_df['orientation'] = pose_3d_df.apply(classify_row_orientation, axis=1)
        
        # Face Orientation Feature
        pose_3d_df['face'] = pose_3d_df.apply(classify_row_face, axis=1)
        
        # 3D Pose Angles Feature
        pose_3d_features_df = compute_connected_joints_angles_3d(pose_3d_df)

        # Rate of Change Features
        pose_3d_features2_df = calculate_pose_angle_difference(pose_3d_features_df)

        # Save Results
        pose_3d_features2_df.to_csv(f'{new_frames_path}/pose_world_data.csv',index=False)

        return pose_2d_features2_df, pose_3d_features2_df
        
    except Exception as e:
        logging.exception("Failed to create pose landmark dictionary")