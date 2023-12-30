import numpy as np

# Data Processing
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

# For sequential analysis

def calculate_pose_angle_difference_per_frame(a1, a2):
    difference = np.abs(a1 - a2)
    return round(difference,4)

def calculate_pose_angle_difference(df):    
    # Initialize the difference columns with zeros
    df['a_head_to_hip_diff'] = 0
    df['a_right_shoulder_to_wrist_diff'] = 0
    df['a_right_hip_to_foot_diff'] = 0
    df['a_left_shoulder_to_wrist_diff'] = 0
    df['a_left_hip_to_foot_diff'] = 0
    
    # Loop through the DataFrame starting from the second row
    for i in range(1, len(df)):
        prev_row, curr_row = df.iloc[i-1], df.iloc[i]
        
        # Calculate the difference in angles between consecutive frames
        df.loc[i, 'a_head_to_hip_diff'] = calculate_pose_angle_difference_per_frame(prev_row['a_head_to_hip'], curr_row['a_head_to_hip'])
        df.loc[i, 'a_right_shoulder_to_wrist_diff'] = calculate_pose_angle_difference_per_frame(prev_row['a_right_shoulder_to_wrist'], curr_row['a_right_shoulder_to_wrist'])
        df.loc[i, 'a_right_hip_to_foot_diff'] = calculate_pose_angle_difference_per_frame(prev_row['a_right_hip_to_foot'], curr_row['a_right_hip_to_foot'])
        df.loc[i, 'a_left_shoulder_to_wrist_diff'] = calculate_pose_angle_difference_per_frame(prev_row['a_left_shoulder_to_wrist'], curr_row['a_left_shoulder_to_wrist'])
        df.loc[i, 'a_left_hip_to_foot_diff'] = calculate_pose_angle_difference_per_frame(prev_row['a_left_hip_to_foot'], curr_row['a_left_hip_to_foot'])

    return df