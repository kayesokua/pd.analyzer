import os

import matplotlib
matplotlib.use('agg')

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import numpy as np

import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

import pandas as pd

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
    
    image_basename = os.path.basename(row['filename']).split('.')[0]
    title = f"{image_basename},{row['orientation']}"
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
        
    
    plot_filename = os.path.join(output_dir, f"{image_basename}.png")
    plt.savefig(plot_filename)
    plt.close()
    
    return plot_filename

def scatter_plot_pose_dictionary_entry(df, index):
    row = df.iloc[index]

    # Extract x and y coordinates
    x_coords = [row[col] for col in df.columns[1:34] if col.endswith('_x')]
    y_coords = [row[col] for col in df.columns[1:34] if col.endswith('_y')]
    
    print(x_coords)
    print(y_coords)
    
    # Create a scatter plot
    scatter = go.Scatter(x=x_coords, y=y_coords, mode='markers', marker=dict(size=8, color='rgba(152, 0, 0, .8)'))

    # Create layout
    layout = go.Layout(
        title="Pose Scatter Plot",
        xaxis=dict(title="X Coordinates"),
        yaxis=dict(title="Y Coordinates"),
        width=800,
        height=600
    )

    # Create figure and add scatter data
    fig = go.Figure(data=[scatter], layout=layout)

    # Return the figure
    return fig

def polar_plot_full_choreography(df, focus):

    if focus == 'right_shoulder':
        joint_names = ['a_right_shoulder_to_wrist','a_right_shoulder_to_elbow','a_right_elbow_to_wrist']
    elif focus == 'right_roc':
        joint_names = sorted([col for col in df.columns if col.startswith('a_right') and col.endswith('_diff')])
    elif focus == 'left':
        joint_names = sorted([col for col in df.columns if col.startswith('a_left') and not col.endswith('_diff')])
    elif focus == 'left_roc':
        joint_names = sorted([col for col in df.columns if col.startswith('a_left') and col.endswith('_diff')])
    else:
        joint_names = ['a_head_to_hip_diff','a_right_shoulder_to_wrist_diff','a_right_hip_to_foot_diff','a_left_shoulder_to_wrist_diff','a_left_hip_to_foot_diff',]
    
    
    fig = make_subplots(rows=3, cols=3, specs=[[{'type': 'polar'}]*3]*3,subplot_titles=joint_names)
    
    for i, joint_name in enumerate(joint_names, 1):
        # Calculate histogram data for each joint angle
        angles = np.deg2rad(df[joint_name].dropna())  # Convert angles to radians and drop NaNs
        hist, bin_edges = np.histogram(angles, bins=36)

        # Plotly polar histogram (barpolar) for each joint
        polar_histogram = go.Barpolar(
            r=hist, 
            theta=np.degrees(bin_edges[:-1]),  # Convert bin edges to degrees
            width=np.diff(np.degrees(bin_edges)),  # Width of each bin
            name=joint_name.replace('_', ' ').title(),
            marker=dict(color='blue', opacity=0.6)
        )
        
        fig.add_trace(polar_histogram, row=(i-1)//3 + 1, col=(i-1)%3 + 1)

    fig.update_layout(
        height=1200,
        width=1200,
        title_text="",
        showlegend=False
    )
    
    
    for annotation in fig['layout']['annotations']:
        annotation['font'] = dict(size=10)

    return fig

import plotly.graph_objects as go

def plot_line_graph_rom(df, title, focus):
    # Define joint names based on the focus area
    if focus == 'upper_right':
        joint_names = ['a_left_shoulder_to_wrist_diff','a_right_shoulder_to_wrist_diff']
    elif focus == 'upper_left':
        joint_names = ['a_left_hip_to_foot_diff','a_right_hip_to_foot_diff']
    elif focus == 'left':
        joint_names = sorted([col for col in df.columns if col.startswith('a_left') and not col.endswith('_diff')])
    elif focus == 'left_roc':
        joint_names = sorted([col for col in df.columns if col.startswith('a_left') and col.endswith('_diff')])
    else:
        joint_names = ['a_head_to_hip_diff','a_right_shoulder_to_wrist_diff','a_right_hip_to_foot_diff','a_left_shoulder_to_wrist_diff','a_left_hip_to_foot_diff']
        
    fig = go.Figure()
    
    for joint_name in joint_names:
        fig.add_trace(go.Scatter(x=df.index, y=df[joint_name], mode='lines', name=joint_name))

    # Update layout
    fig.update_layout(title=title, xaxis_title="Time",yaxis_title="Angle (Degrees)",legend_title="Joints")

    return fig

def interquartile_mean(df, angle_columns):
    iqr_means = {}

    for col in angle_columns:
        # Filter out the zeros before calculating the interquartile range
        non_zero_values = df[col][df[col] != 0]
        Q1 = non_zero_values.quantile(0.50)
        Q3 = non_zero_values.quantile(0.75)
        iqr = non_zero_values[(non_zero_values >= Q1) & (non_zero_values <= Q3)]
        iqr_mean = iqr.mean() if not iqr.empty else None
        iqr_means[col] = iqr_mean

    return iqr_means

def plot_range_of_motion_arc(df):
    fig = go.Figure()

    for col in df.columns:
        if col.startswith('a_') and not col.endswith('_diff'):
            min_angle = np.min(df[col])
            max_angle = np.max(df[col])
            
            # Generate points for the filled area
            theta = np.linspace(min_angle, max_angle, num=30)  # Change num for resolution
            r_inner = np.zeros_like(theta)  # Inner radius (at the center)
            r_outer = np.ones_like(theta) * 5  # Outer radius (you can adjust this value)

            # Combine the inner and outer radii
            r = np.concatenate([r_inner, r_outer[::-1]])
            theta = np.concatenate([theta, theta[::-1]])

            fig.add_trace(go.Scatterpolar(
                r=r,
                theta=theta,
                fill='toself',
                name=col.replace('a_', '').replace('_', ' to ')
            ))

    # Set the layout for the polar chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(showticklabels=False, ticks=''),
            angularaxis=dict(showticklabels=True, ticks='', direction='clockwise', rotation=90)
        )
    )

    return fig

def plotly_table_min_max_rom(df):
    angle_columns = [col for col in df.columns if col.startswith('a_') and col.endswith('_diff')]
    angle_mins = df[angle_columns].replace(0, np.nan).min().rename('Min Angle')
    angle_maxs = df[angle_columns].max().rename('Max Angle')
    angle_means = df[angle_columns].mean().rename('Mean Angle')
    iqr_means = interquartile_mean(df,angle_columns)
           
    rom_stats = pd.DataFrame({
        'connected_joints': angle_columns,
        'min_range': angle_mins.values.round(2),
        'max_range': angle_maxs.values.round(2),
        'mean_range': angle_means.values.round(2),
        'iqr_range': [round(iqr_means[col], 2) for col in angle_columns]
        })
    
    fig = go.Figure(data=[go.Table(
        header=dict(values=['Joint', 'Min Angle', 'Max Angle', 'Mean Angle','Iqr Angle']),
        cells=dict(values=[rom_stats['connected_joints'], rom_stats['min_range'], rom_stats['max_range'],rom_stats['mean_range'], rom_stats['iqr_range']]))
    ])
    fig.update_layout(
        height=200,  # Adjust this height to your preference
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    return fig

def get_table_rom(df):
    angle_columns = [col for col in df.columns if col.startswith('a_') and col.endswith('_diff')]
    angle_mins = df[angle_columns].replace(0, np.nan).min().rename('Min Angle')
    angle_maxs = df[angle_columns].max().rename('Max Angle')
    angle_means = df[angle_columns].mean().rename('Mean Angle')
    iqr_means = interquartile_mean(df,angle_columns)
           
    rom_stats = pd.DataFrame({
        'connected_joints': angle_columns,
        'min_range': angle_mins.values.round(2),
        'max_range': angle_maxs.values.round(2),
        'mean_range': angle_means.values.round(2),
        'iqr_range': [round(iqr_means[col], 2) for col in angle_columns]
        })
    
    return rom_stats.to_dict(orient='records')

def plot_histogram_spatial_orienttion(df, total_duration):
    orientation_count = df['orientation'].value_counts().reset_index()
    orientation_count.columns = ['Orientation', 'Frame Count']
    orientation_count['Duration (Sec)'] = orientation_count['Frame Count'] / len(df) * total_duration
    fig = px.bar(orientation_count, x='Orientation', y='Duration (Sec)')
    return fig