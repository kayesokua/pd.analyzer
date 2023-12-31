import numpy as np

## For 2D Coordinates

def condense_pole_dictionary(row, x_columns, y_columns):
    x = row[x_columns].values
    y = row[y_columns].values
    
    head_x, head_y = x[0:10].mean(), y[0:10].mean()
    chest_x, chest_y = x[[11, 12]].mean(), y[[11, 12]].mean()        
    hip_x, hip_y = x[23:24].mean(), y[23:24].mean()
    knee_right_x, knee_right_y = x[26], y[26]
    foot_right_x, foot_right_y = x[28], y[28]    
    knee_left_x, knee_left_y = x[25], y[25]
    foot_left_x, foot_left_y = x[27], y[27]

    row['head_x'], row['head_y'] = head_x, head_y
    row['chest_x'], row['chest_y'] = chest_x, chest_y
    row['hip_x'], row['hip_y'] = hip_x, hip_y    
    row['knee_right_x'], row['knee_right_y'] = knee_right_x, knee_right_y
    row['foot_right_x'], row['foot_right_y'] = foot_right_x, foot_right_y
    row['knee_left_x'], row['knee_left_y'] = knee_left_x, knee_left_y
    row['foot_left_x'], row['foot_left_y'] = foot_left_x, foot_left_y
    
    return row

def calculate_pose_angle(df, x1, y1, x2, y2):
    angle = np.arctan2(df[y2] - df[y1], df[x2] - df[x1]) * 180 / np.pi
    return round(angle,4)

def compute_connected_joints_angles(pose_df):
    df = pose_df.copy()
    # for range of motion
    df['a_head_to_hip'] = calculate_pose_angle(df, 'head_x', 'head_y', 'hip_x', 'hip_y')
    df['a_right_shoulder_to_wrist'] = calculate_pose_angle(df, 'landmark_12_x', 'landmark_12_y', 'landmark_16_x', 'landmark_16_y')
    df['a_right_hip_to_foot'] = calculate_pose_angle(df, 'landmark_24_x', 'landmark_24_y', 'landmark_28_x', 'landmark_28_y')
    df['a_left_shoulder_to_wrist'] = calculate_pose_angle(df, 'landmark_11_x', 'landmark_11_y', 'landmark_15_x', 'landmark_15_y')
    df['a_left_hip_to_foot'] = calculate_pose_angle(df, 'landmark_23_x', 'landmark_23_y', 'landmark_27_x', 'landmark_27_y')
    
    # for pose recognition
    df['a_nose_to_right_shoulder'] = calculate_pose_angle(df, 'landmark_00_x', 'landmark_00_y', 'landmark_12_x', 'landmark_12_y')
    df['a_right_shoulder_to_elbow'] = calculate_pose_angle(df, 'landmark_12_x', 'landmark_12_y', 'landmark_14_x', 'landmark_14_y')
    df['a_right_elbow_to_wrist'] = calculate_pose_angle(df, 'landmark_14_x', 'landmark_14_y', 'landmark_16_x', 'landmark_16_y')
    df['a_right_shoulder_to_hip'] = calculate_pose_angle(df, 'landmark_12_x', 'landmark_12_y', 'landmark_24_x', 'landmark_24_y')
    df['a_right_hip_to_knee'] = calculate_pose_angle(df, 'landmark_24_x', 'landmark_24_y', 'landmark_26_x', 'landmark_26_y')
    df['a_right_knee_to_foot'] = calculate_pose_angle(df, 'landmark_26_x', 'landmark_26_y', 'landmark_28_x', 'landmark_28_y')
    df['a_nose_to_left_shoulder'] = calculate_pose_angle(df, 'landmark_00_x', 'landmark_00_y', 'landmark_11_x', 'landmark_11_y')
    df['a_left_shoulder_to_elbow'] = calculate_pose_angle(df, 'landmark_11_x', 'landmark_11_y', 'landmark_13_x', 'landmark_13_y')
    df['a_left_elbow_to_wrist'] = calculate_pose_angle(df, 'landmark_13_x', 'landmark_13_y', 'landmark_15_x', 'landmark_15_y')
    df['a_left_shoulder_to_hip'] = calculate_pose_angle(df, 'landmark_11_x', 'landmark_11_y', 'landmark_23_x', 'landmark_23_y')
    df['a_left_hip_to_knee'] = calculate_pose_angle(df, 'landmark_23_x', 'landmark_23_y', 'landmark_25_x', 'landmark_25_y')
    df['a_left_knee_to_foot'] = calculate_pose_angle(df, 'landmark_25_x', 'landmark_25_y', 'landmark_27_x', 'landmark_27_y')
    
    return df

## For 3D Coordinates

def condense_pole_dictionary_3d(row, x_columns, y_columns, z_columns):
    x = row[x_columns].values
    y = row[y_columns].values
    z = row[z_columns].values
    
    head_x, head_y, head_z = x[0:10].mean(), y[0:10].mean(), z[0:10].mean()
    chest_x, chest_y, chest_z = x[[11, 12]].mean(), y[[11, 12]].mean(), z[[11, 12]].mean()     
    hip_x, hip_y, hip_z = x[23:24].mean(), y[23:24].mean(), z[23:24].mean()
    knee_right_x, knee_right_y, knee_right_z = x[26], y[26], z[26]
    foot_right_x, foot_right_y, foot_right_z = x[28], y[28], z[28]
    knee_left_x, knee_left_y, knee_left_z= x[25], y[25], z[25]
    foot_left_x, foot_left_y, foot_left_z = x[27], y[27], z[27]

    row['head_x'], row['head_y'], row['head_z'] = head_x, head_y, head_z
    row['chest_x'], row['chest_y'], row['chest_z'] = chest_x, chest_y, chest_z
    row['hip_x'], row['hip_y'], row['hip_z'] = hip_x, hip_y, hip_z  
    row['knee_right_x'], row['knee_right_y'], row['knee_right_z'] = knee_right_x, knee_right_y, knee_right_z
    row['foot_right_x'], row['foot_right_y'], row['foot_right_z'] = foot_right_x, foot_right_y, foot_right_z
    row['knee_left_x'], row['knee_left_y'], row['knee_left_z'] = knee_left_x, knee_left_y, knee_left_z
    row['foot_left_x'], row['foot_left_y'], row['foot_left_z'] = foot_left_x, foot_left_y, foot_left_z
    
    return row

def calculate_pose_angle_3d(df, x1, y1, z1, x2, y2, z2):
    vector_1 = df[[x1, y1, z1]].values
    vector_2 = df[[x2, y2, z2]].values
    
    # Normalize the vectors
    vector_1_norm = vector_1 / np.linalg.norm(vector_1, axis=1)[:, np.newaxis]
    vector_2_norm = vector_2 / np.linalg.norm(vector_2, axis=1)[:, np.newaxis]
    
    # Calculate the dot product
    dot_product = np.sum(vector_1_norm * vector_2_norm, axis=1)
    
    # Calculate the angle in radians and then convert to degrees
    angle = np.arccos(dot_product) * 180 / np.pi
    
    return np.round(angle, 4)


def compute_connected_joints_angles_3d(pose_df):
    df = pose_df.copy()
    
    # for range of motion
    df['a_head_to_hip'] = calculate_pose_angle_3d(df, 'head_x', 'head_y','head_z', 'hip_x', 'hip_y', 'hip_z')
    df['a_right_shoulder_to_wrist'] = calculate_pose_angle_3d(df, 'landmark_12_x', 'landmark_12_y', 'landmark_12_z', 'landmark_16_x', 'landmark_16_y', 'landmark_16_z')
    df['a_right_hip_to_foot'] = calculate_pose_angle_3d(df, 'landmark_24_x', 'landmark_24_y', 'landmark_24_z', 'landmark_28_x', 'landmark_28_y', 'landmark_28_z')
    df['a_left_shoulder_to_wrist'] = calculate_pose_angle_3d(df, 'landmark_11_x', 'landmark_11_y', 'landmark_11_z', 'landmark_15_x', 'landmark_15_y', 'landmark_15_z')
    df['a_left_hip_to_foot'] = calculate_pose_angle_3d(df, 'landmark_23_x', 'landmark_23_y', 'landmark_23_z', 'landmark_27_x', 'landmark_27_y', 'landmark_27_z')
    
    # for pose recognition
    df['a_nose_to_right_shoulder'] = calculate_pose_angle_3d(df, 'landmark_00_x', 'landmark_00_y', 'landmark_00_z','landmark_12_x', 'landmark_12_y', 'landmark_12_z')
    df['a_right_shoulder_to_elbow'] = calculate_pose_angle_3d(df, 'landmark_12_x', 'landmark_12_y', 'landmark_12_z', 'landmark_14_x', 'landmark_14_y', 'landmark_14_z')
    df['a_right_elbow_to_wrist'] = calculate_pose_angle_3d(df, 'landmark_14_x', 'landmark_14_y', 'landmark_14_z', 'landmark_16_x', 'landmark_16_y', 'landmark_16_z')
    df['a_right_shoulder_to_hip'] = calculate_pose_angle_3d(df, 'landmark_12_x', 'landmark_12_y', 'landmark_12_z',  'landmark_24_x', 'landmark_24_y','landmark_24_z')
    df['a_right_hip_to_knee'] = calculate_pose_angle_3d(df, 'landmark_24_x', 'landmark_24_y', 'landmark_24_z', 'landmark_26_x', 'landmark_26_y', 'landmark_26_z')
    df['a_right_knee_to_foot'] = calculate_pose_angle_3d(df, 'landmark_26_x', 'landmark_26_y', 'landmark_26_z', 'landmark_28_x', 'landmark_28_y', 'landmark_28_z')
    df['a_nose_to_left_shoulder'] = calculate_pose_angle_3d(df, 'landmark_00_x', 'landmark_00_y', 'landmark_00_z', 'landmark_11_x', 'landmark_11_y', 'landmark_11_z')
    df['a_left_shoulder_to_elbow'] = calculate_pose_angle_3d(df, 'landmark_11_x', 'landmark_11_y', 'landmark_11_z', 'landmark_13_x', 'landmark_13_y', 'landmark_13_z')
    df['a_left_elbow_to_wrist'] = calculate_pose_angle_3d(df, 'landmark_13_x', 'landmark_13_y', 'landmark_13_z', 'landmark_15_x', 'landmark_15_y',  'landmark_15_z')
    df['a_left_shoulder_to_hip'] = calculate_pose_angle_3d(df, 'landmark_11_x', 'landmark_11_y', 'landmark_11_z', 'landmark_23_x', 'landmark_23_y', 'landmark_23_z')
    df['a_left_hip_to_knee'] = calculate_pose_angle_3d(df, 'landmark_23_x', 'landmark_23_y', 'landmark_23_z', 'landmark_25_x', 'landmark_25_y', 'landmark_25_z')
    df['a_left_knee_to_foot'] = calculate_pose_angle_3d(df, 'landmark_25_x', 'landmark_25_y', 'landmark_25_z', 'landmark_27_x', 'landmark_27_y', 'landmark_27_z')
        
    return df