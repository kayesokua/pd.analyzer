import os
from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response, send_from_directory
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm,VideoPostForm,CommentForm
from .. import db
from ..models.base import Permission, Role, User, Post, Comment
from ..decorators import admin_required, permission_required
from werkzeug.utils import secure_filename

@main.route('/test', methods=['GET', 'POST'])
def index():
    form = VideoPostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.description.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index_test'))
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.last_updated_on.desc()).paginate(
        page=page, per_page=current_app.config['PDAPP_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('custom/layout_masonry.html', form=form, posts=posts,
                           show_followed=show_followed, pagination=pagination, page=request.path)
    
@main.route('/', methods=['GET'])
def index_test():
    page = request.args.get('page', 1, type=int)
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    pagination = query.order_by(Post.last_updated_on.desc()).paginate(
        page=page, per_page=current_app.config['PDAPP_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('custom/layout_masonry.html', page=request.path, posts=posts, show_followed=show_followed, pagination=pagination)
    
@main.route('/upload', methods=['GET','POST'])
@login_required
def upload_dance_video():
    form = VideoPostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        
        post = Post(author=current_user, title=form.title.data, description=form.description.data)
        db.session.add(post)
        db.session.commit()
        
        ###### Preprocessing
        # Step 0: Save Video with metadata first
        
        ## Make sure user uploads path exists
        rel_user_uploads_path = os.path.join('data', 'uploads', str(current_user.id))
        abs_user_uploads_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_user_uploads_path))
        os.makedirs(abs_user_uploads_path, exist_ok=True)
        
        ## Save the video
        abs_user_post_video_path = os.path.join(abs_user_uploads_path,f'{post.id}.mp4')
        video_file = form.video.data
        video_file.save(abs_user_post_video_path)
        
        # Update video url data
        post.video_filename = os.path.join(f'{str(post.id)}.mp4')
        db.session.commit()
        
        ###### Start Service
        
        # Step 1: Decompose to Frames
        from ..services.converter_video import decompose_video_to_frames
        rel_user_post_processed_path = os.path.join('data', 'processed', str(current_user.id), str(post.id))
        abs_user_post_processed_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_user_post_processed_path))
        os.makedirs(abs_user_post_processed_path, exist_ok=True)
        decompose_video_to_frames(abs_user_post_video_path, abs_user_post_processed_path)
        print(f"{post.id}.mp4 successfully decomposed to frames!")
        
        # Step 2: Pose Landmarker 
        from ..services.pose_landmarker import create_pose_landmark_dictionary
        model_path = os.path.join(current_app.root_path, 'models', 'ml', 'pose_landmarker.task')
        
        pose_norm_data,pose_world_data = create_pose_landmark_dictionary(rel_user_post_processed_path, model_path)
        
        print(f"Successfully landmarked {len(pose_norm_data)} images. Results stored in {rel_user_post_processed_path}/pose_norm_data.csv.")
        print(f"Successfully landmarked {len(pose_world_data)} images. Results stored in {rel_user_post_processed_path}/pose_norm_data.csv.")        
        
        # Step 3: Create Plot Visuals
        from ..services.pose_plot_visualization import plot_2d_coordinates, plot_3d_coordinates
            
        for index, _ in pose_norm_data.iterrows():
            plot_2d_coordinates(pose_norm_data, index, os.path.join(abs_user_post_processed_path, 'plot2d'))
            plot_3d_coordinates(pose_world_data, index, os.path.join(abs_user_post_processed_path, 'plot3d'), azim=120)
        
        print(f"Successfully plotted images for {index} frames. Results stored in {rel_user_post_processed_path}")
        
        from ..services.converter_gif import create_gif_from_folder
        
        # Step 4A: Create 2D Plot Animation
        rel_user_post_plot2d_path = os.path.join(rel_user_post_processed_path,'plot2d')
        abs_user_post_plot2d_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_user_post_plot2d_path))
        
        create_gif_from_folder(abs_user_post_plot2d_path, duration=1000)
        print(f"{rel_user_post_plot2d_path}/animated.mp4 created!")
        
         # Step 4B: Create 3D Plot Animation
        rel_user_post_plot3d_path = os.path.join(rel_user_post_processed_path,'plot3d')
        abs_user_post_plot3d_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_user_post_plot3d_path))
        
        create_gif_from_folder(abs_user_post_plot3d_path, duration=1000)
        print(f"{rel_user_post_plot3d_path}/animated.mp4 created!")
        
        post.video_processed_completed = True
        db.session.commit()
        
        flash('Successfully uploaded! Please see dashboard now..')
        
        return redirect(url_for('dashboard.index'))
    else:
        return render_template('layout_form_basic.html', form=form, page=request.path, page_title="Upload Your Dance Video")

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.last_updated_on.desc()).paginate(
        page=page, per_page=current_app.config['PDAPP_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('custom/layout_user.html', user=user, posts=posts,
                           pagination=pagination, page=request.path)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('layout_form_basic.html', form=form, page_title='Edit Profile', page=request.path)

@main.route('/edit-profile/<uuid:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(str(id))
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    
    return render_template('layout_form_basic.html', form=form, page=request.path, page_title="Edit User Profile", user=user)

@main.route('/post/<uuid:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(str(id))
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been published.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            current_app.config['PDAPP_COMMENTS_PER_PAGE'] + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page=page, per_page=current_app.config['PDAPP_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@main.route('/edit/<uuid:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(str(id))
    if current_user != post.author and \
            not current_user.can(Permission.ADMIN):
        abort(403)
    form = VideoPostForm()
    if form.validate_on_submit():
        post.description = form.description.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.description.data = post.description
    return render_template('layout_form_basic.html', form=form, page=request.path, page_title="Edit Post")


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index_test'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index_test'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index_test'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page=page, per_page=current_app.config['PDAPP_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('layout_followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows, page=request.path, page_title="Your Followers")


@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index_test'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page=page, per_page=current_app.config['PDAPP_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('layout_followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows, page=request.path, page_title="Who Follows You")

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['PDAPP_COMMENTS_PER_PAGE'],
        error_out=False)
    comments = pagination.items
    return render_template('moderate.html', comments=comments,
                           pagination=pagination, page=page)

@main.route('/moderate/enable/<uuid:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(str(id))
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',page=request.args.get('page', 1, type=int)))

@main.route('/moderate/disable/<uuid:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):
    comment = Comment.query.get_or_404(str(id))
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('.moderate',page=request.args.get('page', 1, type=int)))

@main.route('/dataset')
def get_pose_dictionary():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PDAPP_POSES_PER_PAGE']
    rel_path = os.path.join('data', 'external', 'pdictionary_3d.csv')
    abs_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_path))

    try:
        df = pd.read_csv(abs_path)
        total_poses = len(df)
        df_paginated = df.iloc[(page-1)*per_page:page*per_page]  # Paginated data

        posenames = df_paginated['posename'].tolist()
        orientations = df_paginated['orientation'].tolist()
        categories = df_paginated['category'].tolist()
        images = df_paginated['filename'].tolist()
        gif_images = [image[:-4] + '.gif' if image.endswith('.png') else image for image in images]
        
        poses = zip(posenames, orientations, categories, images, gif_images)
        
        total_pages = (total_poses) // per_page
        next_url = url_for('main.get_pose_dictionary', page=page+1) if page < total_pages else None
        prev_url = url_for('main.get_pose_dictionary', page=page-1) if page > 1 else None

        return render_template('dictionary/gallery.html', poses=poses, prev=prev_url, next=next_url, total=total_poses, page=request.path, per_page=per_page, page_title="Poses Dictionary")
    except Exception as e:
        return f"An error occurred: {e}"

@main.route('/dataset/download')
def get_pose_dictionary_table():
    rel_path = os.path.join('data', 'external', 'pdictionary_3d.csv')
    abs_path = os.path.abspath(os.path.join(current_app.root_path, '..', rel_path))
    try:
        df = pd.read_csv(abs_path)
        pose_results = df.to_dict(orient='records')
        return render_template('dictionary/table.html',results=pose_results, page=request.path, page_title="Pose Dictionary (Raw)")
    except Exception as e:
        return f"An error occurred: {e}"


### Serving Files
    
@main.route('/videos/<author_id>/<post_id>', methods=['GET'])
def serve_uploaded_video(author_id,post_id):
    video_filename = str(post_id) + ".mp4"
    print(video_filename)
    data_directory = os.path.abspath(os.path.join(current_app.root_path, '..', 'data', 'uploads'))
    
    rel_filepath = os.path.join(author_id,video_filename)
    print(rel_filepath)
    return send_from_directory(data_directory, rel_filepath)

@main.route('/dictionary/<category>/plot3d/animated/<gif>', methods=['GET'])
def serve_plot3d_object(category,gif):
    data_directory = os.path.abspath(os.path.join(current_app.root_path, '..', 'data', 'external'))
    rel_filepath = os.path.join(category,'plot3d','animated',gif)
    return send_from_directory(data_directory,rel_filepath)

@main.route('/dictionary/<category>/plot2d/<image>', methods=['GET'])
def serve_plot2d_object(category,image):
    data_directory = os.path.abspath(os.path.join(current_app.root_path, '..', 'data', 'external'))
    rel_filepath = os.path.join(category,'plot2d',image)
    return send_from_directory(data_directory,rel_filepath)

@main.route('/dictionary/<category>/annotated/<image>', methods=['GET'])
def serve_annotated_image(category,image):
    data_directory = os.path.abspath(os.path.join(current_app.root_path, '..', 'data', 'external'))
    rel_filepath = os.path.join(category,'annotated',image)
    return send_from_directory(data_directory,rel_filepath)