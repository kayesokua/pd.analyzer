from flask import render_template, request
from flask_login import login_required, current_user
from . import dashboard

@dashboard.route('/', methods=['GET'])
@login_required
def index():
    return render_template("dashboard/index.html", page=request.path)

@dashboard.route('/reports', methods=['GET'])
@login_required
def reports_overview():
    return render_template("dashboard/reports.html", page=request.path)