import os

import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

def plot_2d_coordinates(df, index, output_dir):
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
    
    image_basename = os.path.basename(row['filename']).split('.')[0]
    title = f"pd.analyzer | {image_basename} | {row['orientation']}"
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
    
    os.makedirs(output_dir, exist_ok=True)    
    plot_filename = os.path.join(output_dir, f"{image_basename}.png")
    plt.savefig(plot_filename)
    plt.close()
    
    return plot_filename

def plot_3d_coordinates(df, idx, output_dir):
    row = df.iloc[idx]
    posename = row['posename']
    orientation = row['orientation']
    coordinates = get_3d_coordinates_row_entry(row)

    for azim in range(0, 360, 10):
        fig = plt.figure(figsize=(12, 12))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title(f"pd.analyzer | {posename} | {orientation}")
        
        xs = [point[0] for point in coordinates]
        ys = [point[1] for point in coordinates]
        zs = [point[2] for point in coordinates]

        head_torso_connections = [(0, 1),(13, 14),(0, 13),(0, 14)]
        torso_connections = [(2, 3),(3, 4),(4, 2)]
        
        right_hand_connections = [(6, 15), (6, 16), (15, 16)]
        right_shoulder_connections = [(2, 5), (5, 6)]
        right_leg_connections = [(4, 9), (9, 10)]
        right_foot_connections = [(10, 20), (10, 21),(20,21)]
        
        left_hand_connections = [(8, 17), (8, 18), (17, 18)]
        left_shoulder_connections = [(3, 7), (7, 8)]
        left_leg_connections = [(4, 11), (11, 12)]  
        left_foot_connections = [(12, 22), (12, 23),(22,23)]
        
        ax.scatter(xs, zs, ys, color='black')

        def draw_connections(connections, color):
            for connection in connections:
                x_conn = [xs[connection[0]], xs[connection[1]]]
                y_conn = [ys[connection[0]], ys[connection[1]]]
                z_conn = [zs[connection[0]], zs[connection[1]]]
                ax.plot(x_conn, z_conn, y_conn, color=color, linewidth=2)

        draw_connections(head_torso_connections, 'darkseagreen')
        draw_connections(torso_connections, 'darkolivegreen')
        
        draw_connections(right_hand_connections, 'plum')
        draw_connections(right_shoulder_connections, 'plum')
        draw_connections(right_leg_connections, 'palevioletred')
        draw_connections(right_foot_connections, 'palevioletred')
        
        draw_connections(left_hand_connections, 'skyblue')
        draw_connections(left_shoulder_connections, 'skyblue')
        draw_connections(left_leg_connections, 'steelblue')
        draw_connections(left_foot_connections, 'steelblue')

        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_zlabel("")

        ax.set_xlim(np.min(xs)-0.01,np.max(xs)+0.01)
        ax.set_ylim(np.min(zs)-0.01,np.max(zs)+0.01)
        ax.set_zlim(np.min(ys)-0.01,np.max(ys)+0.01)

        ax.invert_xaxis()
        ax.invert_yaxis()
        ax.invert_zaxis()

        ax.set_xticks(np.arange(np.min(xs)-0.1, np.max(xs)+0.1, 0.1))
        ax.set_yticks(np.arange(np.min(zs)-0.1, np.max(zs)+0.1, 0.1))
        ax.set_zticks(np.arange(np.min(ys)-0.1, np.max(ys)+0.1, 0.1))

        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])

        ax.set_facecolor('white')

        ax.xaxis._axinfo["grid"]['color'] = (0.3, 0.3, 0.3, 0.1)
        ax.yaxis._axinfo["grid"]['color'] = (0.3, 0.3, 0.3, 0.1)
        ax.zaxis._axinfo["grid"]['color'] = (0.3, 0.3, 0.3, 0.1)

        ax.view_init(elev=10, azim=azim)
        
        image_basename = os.path.basename(row['filename']).split('.')[0]
        
        # Ensure the directory exists
        plot_output_dir = os.path.join(output_dir, image_basename)
        os.makedirs(plot_output_dir, exist_ok=True)

        # Save the plot for the current azimuth angle
        plot_filename = f"plot_azim_{azim:03d}.png"
        plot_filepath = os.path.join(plot_output_dir, plot_filename)
        plt.savefig(plot_filepath)
        plt.close(fig)
    
def get_3d_coordinates_row_entry(row):
    coordinates = [
        (row['landmark_00_x'], row['landmark_00_y'], row['landmark_00_z']), #0
        (row['chest_x'], row['chest_y'], row['chest_z']), #1
        (row['landmark_12_x'], row['landmark_12_y'], row['landmark_12_z']), #2
        (row['landmark_11_x'], row['landmark_11_y'], row['landmark_11_z']), #3
        (row['hip_x'], row['hip_y'], row['hip_z']), #4
        (row['landmark_14_x'], row['landmark_14_y'], row['landmark_14_z']), #5
        (row['landmark_16_x'], row['landmark_16_y'], row['landmark_16_z']), #6
        (row['landmark_13_x'], row['landmark_13_y'], row['landmark_13_z']), #7
        (row['landmark_15_x'], row['landmark_15_y'], row['landmark_15_z']), #8
        (row['landmark_26_x'], row['landmark_26_y'], row['landmark_26_z']), #9
        (row['landmark_28_x'], row['landmark_28_y'], row['landmark_28_z']), #10
        (row['landmark_25_x'], row['landmark_25_y'], row['landmark_25_z']), #11
        (row['landmark_27_x'], row['landmark_27_y'], row['landmark_27_z']), #12
        (row['landmark_08_x'], row['landmark_08_y'], row['landmark_08_z']), #13
        (row['landmark_07_x'], row['landmark_07_y'], row['landmark_00_z']), #14
        (row['landmark_18_x'], row['landmark_18_y'], row['landmark_18_z']), #15
        (row['landmark_22_x'], row['landmark_22_y'], row['landmark_22_z']), #16
        (row['landmark_17_x'], row['landmark_17_y'], row['landmark_17_z']), #17
        (row['landmark_21_x'], row['landmark_21_y'], row['landmark_21_z']), #18
        (row['landmark_21_x'], row['landmark_21_y'], row['landmark_21_z']), #19
        (row['landmark_30_x'], row['landmark_30_y'], row['landmark_30_z']), #20
        (row['landmark_32_x'], row['landmark_32_y'], row['landmark_32_z']), #21
        (row['landmark_29_x'], row['landmark_29_y'], row['landmark_29_z']), #22
        (row['landmark_31_x'], row['landmark_31_y'], row['landmark_31_z']), #23
    ]
    return coordinates