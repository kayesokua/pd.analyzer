import os
import pandas as pd

from services.converter_gif import *
from services.data_visualization import plot_2d_coordinates, plot_3d_coordinates
from services.pose_add_features import *
from services.pose_classifier import *
from services.pose_landmarker import create_pose_landmark_dictionary

beginner_poses_path = 'data/external/beginner'
beginner_poses_2d_df,beginner_poses_3d_df = create_pose_landmark_dictionary(beginner_poses_path, "beginner")
for index, _ in beginner_poses_2d_df.iterrows():
    plot_2d_coordinates(beginner_poses_2d_df, index, os.path.join(beginner_poses_path, 'plot2d'))
    plot_3d_coordinates(beginner_poses_3d_df, index, os.path.join(beginner_poses_path, 'plot3d'))
create_gifs_from_folders(os.path.join(beginner_poses_path, "plot3d"))

advanced_poses_path = 'data/external/advanced'
advanced_poses_2d_df,advanced_poses_3d_df = create_pose_landmark_dictionary(advanced_poses_path, "advanced")
for index, _ in advanced_poses_2d_df.iterrows():
    plot_2d_coordinates(advanced_poses_2d_df, index, os.path.join(advanced_poses_path, 'plot2d'))
    plot_3d_coordinates(advanced_poses_3d_df, index, os.path.join(advanced_poses_path, 'plot3d'))
create_gifs_from_folders(os.path.join(advanced_poses_path, "plot3d"))

intermediate_poses_path = 'data/external/intermediate'
intermediate_poses_2d_df,intermediate_poses_3d_df = create_pose_landmark_dictionary(intermediate_poses_path, "intermediate")
for index, _ in intermediate_poses_2d_df.iterrows():
    plot_2d_coordinates(intermediate_poses_2d_df, index, os.path.join(intermediate_poses_path, 'plot2d'))
    plot_3d_coordinates(intermediate_poses_3d_df, index, os.path.join(intermediate_poses_path, 'plot3d'))
create_gifs_from_folders(os.path.join(intermediate_poses_path, "plot3d"))

combined_poses_2d_df = pd.concat([beginner_poses_2d_df,intermediate_poses_2d_df,advanced_poses_2d_df], ignore_index=True)
combined_poses_2d_df.to_csv('data/external/pdictionary_2d.csv',index=False)

combined_poses_3d_df = pd.concat([beginner_poses_2d_df,intermediate_poses_2d_df,advanced_poses_2d_df], ignore_index=True)
combined_poses_3d_df.to_csv('data/external/pdictionary_3d.csv',index=False)