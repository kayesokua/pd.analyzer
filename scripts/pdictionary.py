import os
import re
import numpy as np
import pandas as pd

import cv2

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
matplotlib.use('agg')

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from services.pose_add_features import *
from services.pose_classifier import *
from services.pose_landmarker import draw_landmarks_on_image

def create_pose_landmark_dictionary(input_dir, category):
    base_options = python.BaseOptions(model_asset_path='app/services/models/pose_landmarker.task')
    options = vision.PoseLandmarkerOptions(base_options=base_options,output_segmentation_masks=True)
    landmarker = vision.PoseLandmarker.create_from_options(options)

    filenames = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".png")]
    filenames.sort()
    pose_data = []
    error = 0

    for image_file_path in filenames:
        try:
            image_rgb = cv2.imread(image_file_path, cv2.IMREAD_COLOR)
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_bgr)
            
            detection_result = landmarker.detect(mp_image)
            
            image_basename = os.path.basename(image_file_path).split('.')[0]
            image_basename_modified = re.sub(r'[\d-]', ' ', image_basename)
            
            if detection_result:
                annotated_image = draw_landmarks_on_image(image_bgr, detection_result)
                annotated_image_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
                annotated_image_path = os.path.join(input_dir, 'annotated_' + os.path.basename(image_file_path))
                cv2.imwrite(annotated_image_path, annotated_image_rgb)
                
                plot_filepath = os.path.join(input_dir, 'plot')
                plot_filename = os.path.join(plot_filepath, f'{image_basename}.png')
            
                for pose_landmarks in detection_result.pose_landmarks:
                    pose_info = {
                        'filename': image_file_path,
                        'plot_filename': plot_filename,
                        'annotated_filename': annotated_image_path,
                        'posename': image_basename_modified,
                        'category': category}
                    
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
    
    pose_features_df = pose_df.apply(lambda row: condense_pole_dictionary(row, x_columns, y_columns), axis=1)
    
    pose_features_df['orientation'] = pose_features_df.apply(classify_row_orientation, axis=1)
    
    pose_features2_df = compute_connected_joints_angles(pose_features_df)
    
    pose_features2_df.to_csv(f'{input_dir}/dictionary.csv',index=False)
    print(f"{len(pose_features2_df)} entries processed, {error} entries skipped")

    return pose_features2_df

def basic_plot_pose_dictionary_entry(df, index, output_dir):
    row = df.iloc[index]

    # Spine Alignment
    alignment_x = [row['head_x'], row['chest_x'], row['hip_x']]
    alignment_y = [row['head_y'], row['chest_y'], row['hip_y']]
    
    # Right Arm
    right_arm_x = [row['chest_x'], row['landmark_12_x']]
    right_arm_y = [row['chest_y'], row['landmark_12_y']]
    right_forearm_x = [row['landmark_12_x'], row['landmark_14_x']]
    right_forearm_y = [row['landmark_12_y'], row['landmark_14_y']]
    
    # Left Arm
    left_arm_x = [row['chest_x'], row['landmark_11_x']]
    left_arm_y = [row['chest_y'], row['landmark_11_y']]
    left_forearm_x = [row['landmark_11_x'], row['landmark_13_x']]
    left_forearm_y = [row['landmark_11_y'], row['landmark_13_y']]
    
    # Right Leg
    right_leg_x = [row['hip_x'], row['landmark_26_x']]
    right_leg_y = [row['hip_y'], row['landmark_26_y']]
    right_lower_leg_x = [row['landmark_26_x'], row['foot_right_x']]
    right_lower_leg_y = [row['landmark_26_y'], row['foot_right_y']]
    
    # Left Leg
    left_leg_x = [row['hip_x'], row['landmark_25_x']]
    left_leg_y = [row['hip_y'], row['landmark_25_y']]
    left_lower_leg_x = [row['landmark_25_x'], row['foot_left_x']]
    left_lower_leg_y = [row['landmark_25_y'], row['foot_left_y']]

    # Create plot
    fig, ax = plt.subplots(figsize=(8, 8))
    
    title = f"{row['posename']},{row['orientation']}"
    ax.set_title(title)

    # Spine
    ax.plot(alignment_x, alignment_y, color=mcolors.CSS4_COLORS['green'], label="Spine", marker='_', alpha=0.2)
    ax.scatter(row['head_x'], row['head_y'], color=mcolors.CSS4_COLORS['green'], label="Head")
    ax.scatter(row['chest_x'], row['chest_y'], color=mcolors.CSS4_COLORS['green'], label="Upper Torso")
    ax.scatter(row['hip_x'], row['hip_y'], color=mcolors.CSS4_COLORS['green'], label="Hips")
    
    # Right Arm
    ax.plot(right_arm_x, right_arm_y, color=mcolors.CSS4_COLORS['red'], label="Right Arm", marker='_', alpha=0.2)
    ax.plot(right_forearm_x, right_forearm_y, color=mcolors.CSS4_COLORS['red'], label="Right Forearm", marker='_', alpha=0.2)
    ax.scatter(row['landmark_12_x'], row['landmark_12_y'], color=mcolors.CSS4_COLORS['red'], label="Right Shoulder")
    ax.scatter(row['landmark_14_x'], row['landmark_14_y'], color=mcolors.CSS4_COLORS['red'], label="Right Wrist")
    
    # Right Leg
    ax.plot(right_leg_x, right_leg_y, color=mcolors.CSS4_COLORS['red'], label="Right Leg", marker='_', alpha=0.2)
    ax.plot(right_lower_leg_x, right_lower_leg_y, color=mcolors.CSS4_COLORS['red'], label="Right Leg", marker='_', alpha=0.2)
    ax.scatter(row['landmark_26_x'], row['landmark_26_y'], color=mcolors.CSS4_COLORS['red'], label="Right Knee")
    ax.scatter(row['foot_right_x'], row['foot_right_y'], color=mcolors.CSS4_COLORS['red'], label="Right Foot")
    
    # Left Arm
    ax.plot(left_arm_x, left_arm_y, color=mcolors.CSS4_COLORS['blue'], label="Left Arm", marker='_', alpha=0.2)
    ax.plot(left_forearm_x, left_forearm_y, color=mcolors.CSS4_COLORS['blue'], label="Left Arm", marker='_', alpha=0.2)
    ax.scatter(row['landmark_11_x'], row['landmark_11_y'], color=mcolors.CSS4_COLORS['blue'], label="Left Shoulder")
    ax.scatter(row['landmark_13_x'], row['landmark_13_y'], color=mcolors.CSS4_COLORS['blue'], label="Left Wrist")
    
    # Left Leg
    ax.plot(left_leg_x, left_leg_y, color=mcolors.CSS4_COLORS['blue'], label="Left Leg", marker='_', alpha=0.2)
    ax.plot(left_lower_leg_x, left_lower_leg_y, color=mcolors.CSS4_COLORS['blue'], label="Left Leg", marker='_', alpha=0.2)
    ax.scatter(row['landmark_25_x'], row['landmark_25_y'], color=mcolors.CSS4_COLORS['blue'], label="Left Knee")
    ax.scatter(row['foot_left_x'], row['foot_left_y'], color=mcolors.CSS4_COLORS['blue'], label="Left Foot")

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.invert_yaxis()
    ax.set_xticks(np.arange(0, 1.05, 0.05))
    ax.set_yticks(np.arange(0, 1.05, 0.05))
    ax.grid(True)
    ax.grid(which='both', color='gray', linestyle='--', linewidth=0.5)
    
    fig.tight_layout()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    image_basename = os.path.basename(row['filename']).split('.')[0]
    plot_filename = os.path.join(output_dir, f"{image_basename}.png")
    plt.savefig(plot_filename)
    plt.close()
    
    return plot_filename

beginner_poses_path = 'data/external/beginner'
beginner_poses_df = create_pose_landmark_dictionary(beginner_poses_path, "beginner")
for index, _ in beginner_poses_df.iterrows():
    basic_plot_pose_dictionary_entry(beginner_poses_df, index, os.path.join(beginner_poses_path, 'plot'))

intermediate_poses_path = 'data/external/intermediate'
intermediate_poses_df = create_pose_landmark_dictionary('data/external/intermediate', "intermediate")
for index, _ in intermediate_poses_df.iterrows():
    basic_plot_pose_dictionary_entry(intermediate_poses_df, index, os.path.join(intermediate_poses_path, 'plot'))

advanced_poses_path = 'data/external/advanced'
advanced_poses_df = create_pose_landmark_dictionary('data/external/advanced', "advanced")
for index, _ in advanced_poses_df.iterrows():
    basic_plot_pose_dictionary_entry(advanced_poses_df, index, os.path.join(advanced_poses_path, 'plot'))

combined_poses_df = pd.concat([beginner_poses_df, intermediate_poses_df, advanced_poses_df], ignore_index=True)
combined_poses_df.to_csv('data/external/pdictionary.csv',index=False)