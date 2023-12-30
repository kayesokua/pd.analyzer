from flask import jsonify, request, g, url_for, current_app, send_from_directory
from .. import db
from ..models.base import Post, Permission
from . import api
from .decorators import permission_required
from .errors import forbidden

@api.route('/dictionary')
def get_pose_dictionary():
    return "dictionary poses here"