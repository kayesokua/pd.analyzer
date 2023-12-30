from flask import render_template, request
from . import dashboard

@dashboard.route('/', methods=['GET'])
def index():
    return render_template('dashboard/results.html', page=request.path)

@dashboard.route('/report/<post_id>', methods=['GET'])
def individual_report(post_id):
    post_id = post_id
    return f'Reporting for {post_id}'