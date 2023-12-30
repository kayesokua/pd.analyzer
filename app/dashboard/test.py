# from flask import Flask, Blueprint, request, render_template, url_for, redirect, send_file,json

# from services.converter_video import *
# from services.converter_gif import *
# from services.pose_landmarker import *
# from services.pose_recognition import *
# from services.data_visualization import *

# import pytz

# import plotly
# import plotly.express as px
# import pandas as pd
# import json

# import os

# bp = Blueprint("accounts", __name__, url_prefix="/dashboard")
# tz = pytz.timezone('UTC')


# @bp.route('/')
# def dashboard_home():
#     samples_filepath = os.path.join('data','processed')
#     sample_ids = [d for d in os.listdir(samples_filepath) if os.path.isdir(os.path.join(samples_filepath, d))]
#     return "A summary of all your dancing over time"
#     # return render_template("landing.html", page_title="Home", page=request.path, sample_ids=sample_ids)

# @bp.route('/results/<path:filename>/table')
# def display_results_table(filename):
#     filepath = os.path.join('data','processed', filename, 'results.csv')
#     try:
#         df = pd.read_csv(filepath)
#         pose_results = df.to_dict(orient='records')
#         return render_template('results_table.html',results=pose_results, video_id=filename, page=request.path, page_title="Analysis Results")
#     except Exception as e:
#         return f"An error occurred: {e}"

# @bp.route('/results/<path:filename>')
# def display_results_chart(filename):
#     filepath = os.path.join('data', 'processed', filename, 'results.csv')
    
#     try:
#         df = pd.read_csv(filepath)
        
#         orientation_count = df['orientation'].value_counts().reset_index()
#         orientation_count.columns = ['Pose', 'Count']
#         fig_spatial_orientation = px.bar(orientation_count, x='Pose', y='Count', title='Pose Classification Counts')
#         plotly_so = json.dumps(fig_spatial_orientation, cls=plotly.utils.PlotlyJSONEncoder)
        
#         # Min and Max Range of Motion
#         angle_columns = [col for col in df.columns if col.startswith('a_') and col.endswith('_diff')]
#         angle_mins = df[angle_columns].replace(0, np.nan).min().rename('Min Angle')
#         angle_maxs = df[angle_columns].max().rename('Max Angle')
#         angle_means = df[angle_columns].mean().rename('Mean Angle')
#         iqr_means = interquartile_mean(df,angle_columns)
           
#         rom_stats = pd.DataFrame({
#             'connected_joints': angle_columns,
#             'min_range': angle_mins.values,
#             'max_range': angle_maxs.values,
#             'mean_range': angle_means.values,
#             'iqr_range': [iqr_means[col] for col in angle_columns]
#         })

#         fig_range_of_motion = go.Figure(data=[go.Table(
#             header=dict(values=['Joint', 'Min Angle', 'Max Angle', 'Mean Angle','Iqr Angle']),
#             cells=dict(values=[rom_stats['connected_joints'], rom_stats['min_range'], rom_stats['max_range'],rom_stats['mean_range'], rom_stats['iqr_range']]))
#         ])
#         fig_range_of_motion.update_layout(margin=dict(l=0, r=0, t=0, b=0))
#         plotly_rom = json.dumps(fig_range_of_motion, cls=plotly.utils.PlotlyJSONEncoder)
        
        
#         # Range of Motion Over Time
#         plotly_rom_over_time = {}

#         for col in angle_columns:
#             df[f'{col}_diff'] = df[col].diff().fillna(0)
                    
#         for col in angle_columns:
#             fig = px.line(df, y=f'{col}_diff', title=f'Angle Differences Over Time for {col}')
#             plotly_rom_over_time[col] = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        
#         # Visibility of Poses Quality
#         v_columns = [col for col in df.columns if col.endswith('_v')]
#         all_v_scores = pd.concat([df[col] for col in v_columns])
#         bins = np.arange(0.1, 1.1, 0.1)
#         all_v_scores_bins = pd.cut(all_v_scores, bins, include_lowest=True, right=True)

#         # Convert Interval objects to strings
#         visibility_count = all_v_scores_bins.value_counts().reset_index()
#         visibility_count['index'] = visibility_count['index'].astype(str)
#         visibility_count.columns = ['Visibility Score Range', 'Count']

#         fig_visibility = px.bar(visibility_count, x='Visibility Score Range', y='Count', title='Total Distribution of Visibility Scores')
#         plotly_v = json.dumps(fig_visibility, cls=plotly.utils.PlotlyJSONEncoder)

#         #Display GIF
#         gif_filepath = os.path.join('data', 'processed', filename, 'animation.gif')
        
#         # Render the template with both charts
#         return render_template('results.html',
#                                plotly_so=plotly_so,
#                                plotly_rom=plotly_rom,
#                                plotly_v=plotly_v,
#                                plotly_rom_over_time=plotly_rom_over_time,
#                                video_id=filename,
#                                page=request.path,
#                                gif_filepath=gif_filepath,
#                                page_title="Choreography Summary")

#     except Exception as e:
#         return f"An error occurred: {str(e)}"
    

# @bp.route('/results/<path:filename>/images')
# def display_results_images(filename):
#     filepath = os.path.join('data', 'processed', filename, 'results.csv')
#     try:
#         df = pd.read_csv(filepath)
#         image_files = df['annotated_filename'].tolist()
#         orientations = df['orientation'].tolist()
#         image_data = zip(image_files, orientations)
#         return render_template('results_images.html', image_data=image_data, video_id=filename,  page=request.path,  page_title="Analysis Results")
    
#     except Exception as e:
#         return f"An error occurred: {e}"
    
# @bp.route('/results/<path:filename>/coordinates')
# def display_results_coordinates(filename):
#     images_dir = os.path.join('data', 'processed', filename, 'plot')
#     try:
#         image_files = sorted(glob.glob(os.path.join(images_dir, '*.png')))
#         image_filenames = [os.path.join(images_dir, os.path.basename(file)) for file in image_files]
#         return render_template('results_plot.html', image_files=image_filenames, video_id=filename, page=request.path, page_title="Analysis Results")
#     except Exception as e:
#         return f"An error occurred: {e}"

# @bp.route('/results/<path:filename>/polar')
# def display_results_polar_plot(filename):
#     filepath = os.path.join('data','processed', filename, 'results.csv')
#     try:
#         df = pd.read_csv(filepath)
#         fig = polar_plot_full_choreography(df)
#         graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#         return render_template('results_polarplot.html', graphJSON=graphJSON, video_id=filename, page=request.path, page_title="Analysis Results")
#     except Exception as e:
#         return f"An error occurred: {e}"
    
# @bp.route('/results/<path:filename>/distances')
# def display_results_pose_distances(filename):
#     filepath = os.path.join('data', 'processed', filename, 'results.csv')
#     poses_df = os.path.join('data','external', 'combined_dictionary.csv')
    
#     try:
#         df = pd.read_csv(filepath)
#         poses_df = pd.read_csv(poses_df)        
#         closest_matches = find_closest_match_per_frame(df, poses_df)

#         return render_template('results_poses.html',
#                                closest_matches=closest_matches,
#                                video_id=filename, 
#                                page=request.path,
#                                page_title="Poses by Closest Average Distance")

#     except Exception as e:
#         return f"An error occurred: {e}"
    
# @bp.route('/results/<path:filename>/angles')
# def display_results_pose_angles(filename):
#     filepath = os.path.join('data', 'processed', filename, 'results.csv')
#     dictionary_filepath = os.path.join('data','external', 'combined_dictionary.csv')
    
#     try:
#         df = pd.read_csv(filepath)
#         poses_df = pd.read_csv(dictionary_filepath)   
#         closest_matches = find_closest_angles_per_frame(df, poses_df)

#         return render_template('results_poses.html',
#                                closest_matches=closest_matches,
#                                video_id=filename, 
#                                page=request.path,
#                                page_title="Poses by Closest Average Angles")

#     except Exception as e:
#         return f"An error occurred: {e}"

# @bp.route('/<path:filename>')
# def send_image(filename):
#     return send_file(filename)