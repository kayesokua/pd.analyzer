import numpy as np

def get_spin_count(pose_world_data):
    z_columns = ['head_z','chest_z','hip_z']
    faces = []
    for index, row in pose_world_data[z_columns].iterrows():
        if np.mean(row) < 0: #If negative, it is front
            faces.append('front')
        else:
            faces.append('back')
            
    spin_count = 0
    
    for i in range(len(faces) - 1):
        if faces[i] != faces[i + 1]:
            spin_count += 1

    return spin_count - 1