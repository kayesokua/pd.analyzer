from flask import render_template, request, current_app
from . import api
import os
import pandas as pd

# @api.route('/dictionary')
# def get_pose_dictionary():
#     rel_path = os.path.join('data', 'external', 'pdictionary_3d.csv')
#     abs_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_path))
    
#     try:
#         df = pd.read_csv(abs_path)
#         images = df['filename'].tolist()
#         orientations = df['orientation'].tolist()
#         categories = df['category'].tolist()
#         pose_data = zip(images, orientations, categories)
#         return render_template('dictionary/gallery.html', pose_data=pose_data,  page=request.path,  page_title="Poses Dictionary")
    
#     except Exception as e:
#         return f"An error occurred: {e}"

# @api.route('/dictionary/table')
# def get_pose_dictionary_table():
#     rel_path = os.path.join('data', 'external', 'pdictionary_3d.csv')
#     abs_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_path))
    
#     try:
#         df = pd.read_csv(abs_path)
#         pose_results = df.to_dict(orient='records')
#         return render_template('dictionary/table.html',results=pose_results, page=request.path, page_title="Dictionary Results")
#     except Exception as e:
#         return f"An error occurred: {e}"