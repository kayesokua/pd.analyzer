import numpy as np
import os

def compute_angle_difference(angle1, angle2):
    difference = np.abs(angle2 - angle1)
    return round(difference,4)
    
def compute_angles_matrix(m1, m2):
    m1, m2 = m1.squeeze(), m2.squeeze()

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
    
    df['filename'] = df['filepath_abs'].apply(lambda x: os.path.basename(x))
        
    for i in range(len(df)):
        frame_distances = []
        m1 = df.iloc[i]

        # Filter poses_df based on the orientation of m1
        filtered_poses_df = poses_df[poses_df['orientation'] == m1['orientation']]

        for j in range(len(filtered_poses_df)):
            m2 = filtered_poses_df.iloc[j]            
            soln = compute_angles_matrix(m1, m2)
            soln_avg = np.sum(soln)
            soln_set = (soln_avg,
                        df.iloc[i]['filename'],
                        m2['filename'],
                        m2['posename'],
                        m2['category'])
            frame_distances.append(soln_set)
    
        if frame_distances:
            closest_match = min(frame_distances, key=lambda x: x[0])
            closest_matches.append((i, closest_match[0], closest_match[1], closest_match[2], closest_match[3], closest_match[4]))
        else:
            print(f"No valid distances found for frame {i}.")
            closest_matches.append((i, None, None, None, None, None))
    
    return closest_matches
