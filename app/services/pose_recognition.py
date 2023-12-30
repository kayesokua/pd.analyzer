import numpy as np

def compute_angle_difference(angle1, angle2):
    difference = np.abs(angle2 - angle1)
    return round(difference,4)
    
def compute_angles_matrix(m1, m2):
    m1, m2 = m1.squeeze(), m2.squeeze()
    
    # d1 = compute_angle_difference(m1['a_head_to_hip'],m2['a_head_to_hip'])
    # d2 = compute_angle_difference(m1['a_right_shoulder_to_wrist'],m2['a_right_shoulder_to_wrist'])
    # d3 = compute_angle_difference(m1['a_right_hip_to_foot'],m2['a_right_hip_to_foot'])
    # d4 = compute_angle_difference(m1['a_left_shoulder_to_wrist'],m2['a_left_shoulder_to_wrist'])
    # d5 = compute_angle_difference(m1['a_left_hip_to_foot'],m2['a_left_hip_to_foot'])
    
    r1 = compute_angle_difference(m1['a_nose_to_right_shoulder'],m2['a_nose_to_right_shoulder'])
    r2 = compute_angle_difference(m1['a_right_shoulder_to_elbow'],m2['a_right_shoulder_to_elbow'])
    r3 = compute_angle_difference(m1['a_right_elbow_to_wrist'],m2['a_right_elbow_to_wrist'])
    r4 = compute_angle_difference(m1['a_right_shoulder_to_hip'],m2['a_right_shoulder_to_hip'])
    r5 = compute_angle_difference(m1['a_right_hip_to_knee'],m2['a_right_hip_to_knee'])
    r6 = compute_angle_difference(m1['a_right_knee_to_foot'],m2['a_right_knee_to_foot'])
    
    l1 = compute_angle_difference(m1['a_nose_to_left_shoulder'],m2['a_nose_to_left_shoulder'])
    l2 = compute_angle_difference(m1['a_left_shoulder_to_elbow'],m2['a_left_shoulder_to_elbow'])
    l3 = compute_angle_difference(m1['a_left_elbow_to_wrist'],m2['a_left_elbow_to_wrist'])
    l4 = compute_angle_difference(m1['a_left_shoulder_to_hip'],m2['a_left_shoulder_to_hip'])
    l5 = compute_angle_difference(m1['a_left_hip_to_knee'],m2['a_left_hip_to_knee'])
    l6 = compute_angle_difference(m1['a_left_knee_to_foot'],m2['a_left_knee_to_foot'])
    
    return [r1,r2,r3,r4,r5,r6,l1,l2,l3,l4,l5,l6]

def find_closest_angles_per_frame(df, poses_df):
    closest_matches = []
        
    for i in range(len(df)):
        frame_distances = []
        m1 = df.iloc[i]
        
        for j in range(len(poses_df)):
            m2 = poses_df.iloc[j]            
            soln = compute_angles_matrix(m1, m2)
            soln_avg=np.sum(soln)
            soln_set = (soln_avg, df.iloc[i]['annotated_filename'], df.iloc[i]['plot_filename'], poses_df.iloc[j]['plot_filename'], poses_df.iloc[j]['posename'],poses_df.iloc[j]['category'])
            frame_distances.append(soln_set)
            
        # for distance in frame_distances:
        #     print(f"Frame {i}, Distance: {distance}")

        if frame_distances:
            closest_match = min(frame_distances, key=lambda x: x[0])
            closest_matches.append((i, closest_match[0], closest_match[1], closest_match[2], closest_match[3],closest_match[4],closest_match[5]))
        else:
            print(f"No valid distances found for frame {i}.")
            closest_matches.append((i, None, None, None))
    
    return closest_matches

def compute_euclidean_distance(x1, y1, x2, y2):
  dx = x2 - x1
  dy = y2 - y1
  distance = np.sqrt(dx**2 + dy**2)
  return round(distance,4)

def compute_distances_matrix(m1, m2):
    m1, m2 = m1.squeeze(), m2.squeeze()
    
    # Nose
    d1 = compute_euclidean_distance(m1['landmark_00_x'],m1['landmark_00_y'],m2['landmark_00_x'],m2['landmark_00_y'])
    
    # Four Squres of the Torso
    d2 = compute_euclidean_distance(m1['landmark_11_x'],m1['landmark_11_y'],m2['landmark_11_x'],m2['landmark_11_y'])
    d3 = compute_euclidean_distance(m1['landmark_12_x'],m1['landmark_12_y'],m2['landmark_12_x'],m2['landmark_12_y'])
    d4 = compute_euclidean_distance(m1['landmark_23_x'],m1['landmark_23_y'],m2['landmark_23_x'],m2['landmark_23_y'])
    d5 = compute_euclidean_distance(m1['landmark_24_x'],m1['landmark_24_y'],m2['landmark_24_x'],m2['landmark_24_y'])
    
    # Elbows and Wrists
    d6 = compute_euclidean_distance(m1['landmark_13_x'],m1['landmark_13_y'],m2['landmark_13_x'],m2['landmark_13_y'])
    d7 = compute_euclidean_distance(m1['landmark_14_x'],m1['landmark_14_y'],m2['landmark_14_x'],m2['landmark_14_y'])
    d8 = compute_euclidean_distance(m1['landmark_15_x'],m1['landmark_15_y'],m2['landmark_15_x'],m2['landmark_15_y'])
    d9 = compute_euclidean_distance(m1['landmark_16_x'],m1['landmark_16_y'],m2['landmark_16_x'],m2['landmark_16_y'])
    
    # Knees and Feet
    d10 = compute_euclidean_distance(m1['landmark_25_x'],m1['landmark_25_y'],m2['landmark_25_x'],m2['landmark_25_y'])
    d11 = compute_euclidean_distance(m1['landmark_26_x'],m1['landmark_26_y'],m2['landmark_26_x'],m2['landmark_26_y'])
    d12 = compute_euclidean_distance(m1['landmark_27_x'],m1['landmark_27_y'],m2['landmark_27_x'],m2['landmark_27_y'])
    d13 = compute_euclidean_distance(m1['landmark_28_x'],m1['landmark_28_y'],m2['landmark_28_x'],m2['landmark_28_y'])
    
    return [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13]

def find_closest_match_per_frame(df, poses_df):
    closest_matches = []
    
    for i in range(len(df)):
        frame_distances = []
        m1 = df.iloc[i]  # Current frame as a Series

        for j in range(len(poses_df)):
            m2 = poses_df.iloc[j]  # Potential match as a Series
            soln = compute_distances_matrix(m1, m2)
            soln_avg = np.mean(soln)
            frame_distances.append((soln_avg, df.iloc[i]['filename'], poses_df.iloc[j]['filename']))

        closest_match = min(frame_distances, key=lambda x: x[0])
        closest_matches.append((i, closest_match[0], closest_match[1],closest_match[2]))
    
    return closest_matches