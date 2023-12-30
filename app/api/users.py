from flask import jsonify, request, current_app, url_for
from . import api
from ..models.base import User, Post


@api.route('/users/<uuid:id>')
def get_user(id):
    user = User.query.get_or_404(str(id))
    return jsonify(user.to_json())


@api.route('/users/<uuid:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(str(id))
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.last_updated_on.desc()).paginate(
        page=page, per_page=current_app.config['PDAPP_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/users/<uuid:id>/timeline/')
def get_user_followed_posts(id):
    user = User.query.get_or_404(str(id))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.last_updated_on.desc()).paginate(
        page=page, per_page=current_app.config['PDAPP_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_followed_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
