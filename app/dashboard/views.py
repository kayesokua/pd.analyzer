from flask import render_template, request, send_file, current_app
from flask_login import login_required
from .. import db
from ..models.base import Post, User
from . import dashboard
import os
import pandas as pd

import plotly
import plotly.express as px
import json

from ..services.data_visualization import plot_histogram_spatial_orienttion,plot_range_of_motion_arc, get_table_rom, plotly_table_min_max_rom
from ..services.report_calculation import get_spin_count
    
@dashboard.route('/<username>', methods=['GET'])
@login_required
def index(username):
    user = User.query.filter_by(username=username).first_or_404() 
    posts = user.posts.order_by(Post.last_updated_on.desc())
    aggregated_data = []
    total_frames = 0
    total_duration = 0
    total_spins = 0
    for post in posts:
        properties_str = post.video_properties
        properties_str_reformatted = properties_str.replace("'", '"')
        properties_json = json.loads(properties_str_reformatted)
        
        rel_user_post_processed_path = os.path.join('data', 'processed', str(post.author_id), str(post.id))
        abs_user_post_processed_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_user_post_processed_path))
        pose_world_data_path = os.path.join(abs_user_post_processed_path, 'pose_world_data.csv')    
        
        pose_world_data_df = pd.read_csv(pose_world_data_path)
        
        # Get All Data
        aggregated_data.append(pose_world_data_df)
        total_frames += len(pose_world_data_df)
        total_duration += properties_json['duration']
        total_spins += get_spin_count(pose_world_data_df)
    
    combined_df = pd.concat(aggregated_data, ignore_index=True)

    # Spatial Orientation Chart
    fig_spatial_orientation = plot_histogram_spatial_orienttion(combined_df, total_duration)
    plotly_so = json.dumps(fig_spatial_orientation, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Plot ROM Arc
    fig_rom_arc = plot_range_of_motion_arc(combined_df)
    plotly_rom_arc = json.dumps(fig_rom_arc, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Get Min and Max ROM Table
    fig_range_of_motion = plotly_table_min_max_rom(combined_df)
    plotly_rom_table = json.dumps(fig_range_of_motion, cls=plotly.utils.PlotlyJSONEncoder)
    
    rom_data = get_table_rom(combined_df)
        
    hours, remainder = divmod(int(total_duration), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    total_duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"
    
    return render_template('dashboard/index.html',
                           user=user,
                           posts=posts,
                           rom_data=rom_data,
                           plotly_so=plotly_so,
                           plotly_rom_table=plotly_rom_table,
                           plotly_rom_arc=plotly_rom_arc,
                           total_frames=total_frames,
                           total_duration=total_duration_str,
                           total_spins=total_spins,
                           page=request.path)

@dashboard.route('/reports/<username>', methods=['GET'])
@login_required
def reports_overview(username):
    user = User.query.filter_by(username=username).first_or_404() 
    posts = user.posts.order_by(Post.last_updated_on.desc())
    return render_template('dashboard/reports.html', user=user, posts=posts, page=request.path)

@dashboard.route('/page/<uuid:id>', methods=['GET', 'POST'])
@login_required
def report_page(id):
    post = Post.query.get_or_404(str(id))
    
    properties_str = post.video_properties
    properties_str_reformatted = properties_str.replace("'", '"')
    properties_json = json.loads(properties_str_reformatted)
    
    rel_user_post_processed_path = os.path.join('data', 'processed', str(post.author_id), str(post.id))
    abs_user_post_processed_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_user_post_processed_path))
    pose_world_data_path = os.path.join(abs_user_post_processed_path, 'pose_world_data.csv')    
    
    pose_world_data_df = pd.read_csv(pose_world_data_path)
    pose_world_data_df = pose_world_data_df.drop(columns=['filepath_abs'], axis=1)
    
    # Get All Data
    
    total_frame_entries = len(pose_world_data_df)
    total_frames_processed = round(total_frame_entries / int(properties_json['frames']),2) * 100
    
    total_duration = properties_json['duration']
    
    
    hours, remainder = divmod(int(total_duration), 3600)
    minutes, seconds = divmod(remainder, 60)
    total_duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"
    
    # Display Tabular Data
    pose_world_data = pose_world_data_df.to_dict(orient='records')
    
    # Spatial Orientation Chart
    fig_spatial_orientation = plot_histogram_spatial_orienttion(pose_world_data_df, total_duration)
    plotly_so = json.dumps(fig_spatial_orientation, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Plot ROM Arc
    fig_rom_arc = plot_range_of_motion_arc(pose_world_data_df)
    plotly_rom_arc = json.dumps(fig_rom_arc, cls=plotly.utils.PlotlyJSONEncoder)
    
    
    
    # Get Min and Max ROM Table
    rom_data = get_table_rom(pose_world_data_df)
    
    
    total_spins = get_spin_count(pose_world_data_df)
    
    return render_template('dashboard/report_individual.html',
                           posts=[post],
                           plotly_so=plotly_so,
                           rom_data=rom_data,
                           plotly_rom_arc=plotly_rom_arc,
                           total_spins=total_spins,
                           total_frame_entries=total_frame_entries,
                           total_frames_processed=total_frames_processed,
                           total_duration=total_duration_str,
                           pose_world_data=pose_world_data,
                           page=request.path,
    )

@dashboard.route('/page/<uuid:id>/table', methods=['GET', 'POST'])
@login_required
def report_page_display_raw_data(id):
    post = Post.query.get_or_404(str(id))
    
    rel_user_post_processed_path = os.path.join('data', 'processed', str(post.author_id), str(post.id))
    abs_user_post_processed_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_user_post_processed_path))
    pose_world_data_path = os.path.join(abs_user_post_processed_path, 'pose_world_data.csv')    
    
    pose_world_data_df = pd.read_csv(pose_world_data_path)
    pose_world_data_df = pose_world_data_df.drop(columns=['filepath_abs'], axis=1)    
    pose_world_data = pose_world_data_df.to_dict(orient='records')
    
    return render_template('dashboard/report_table.html',
                           posts=[post],
                           pose_world_data=pose_world_data,
                           page=request.path)
    
@dashboard.route('/page/<uuid:id>/matches', methods=['GET', 'POST'])
def report_page_display_matches(id):
    post = Post.query.get_or_404(str(id))

    rel_user_post_processed_path = os.path.join('data', 'processed', str(post.author_id), str(post.id))
    abs_user_post_processed_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_user_post_processed_path))
    pose_world_data_path = os.path.join(abs_user_post_processed_path, 'pose_world_data.csv')    
    
    rel_dictionary_path = os.path.join('data', 'external')
    abs_dictionary_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_dictionary_path))
    pdictionary_path = os.path.join(abs_dictionary_path, 'pdictionary_3d.csv')    
    
    pose_world_data_df = pd.read_csv(pose_world_data_path)
    pdictionary = pd.read_csv(pdictionary_path)    
    
    from ..services.pose_recognition import find_closest_angles_per_frame
    closest_matches = find_closest_angles_per_frame(pose_world_data_df, pdictionary)

    return render_template('dashboard/report_matches.html',
                           closest_matches=closest_matches,
                           posts=[post],
                           page=request.path,
                           page_title="Poses by Closest Average Distance")
    
    
@dashboard.route('download/data/<uuid:id>/world')
@login_required
def download_pose_world_data(id):
    post = Post.query.get_or_404(str(id))
    rel_user_post_processed_path = os.path.join('data', 'processed', str(post.author_id), str(post.id))
    abs_user_post_processed_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_user_post_processed_path))
    pose_world_data_path = os.path.join(abs_user_post_processed_path, 'pose_world_data.csv')
    return send_file(pose_world_data_path, as_attachment=True)

@dashboard.route('download/data/<uuid:id>/normalized')
@login_required
def download_pose_norm_data(id):
    post = Post.query.get_or_404(str(id))
    rel_user_post_processed_path = os.path.join('data', 'processed', str(post.author_id), str(post.id))
    abs_user_post_processed_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_user_post_processed_path))
    pose_norm_data_path = os.path.join(abs_user_post_processed_path, 'pose_norm_data.csv')
    return send_file(pose_norm_data_path, as_attachment=True)