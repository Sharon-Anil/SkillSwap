from datetime import datetime
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from . import db
from .models import User, Video, ViewerUnlock
from sqlalchemy import func

main = Blueprint('main', __name__)

# Upload folders
VIDEO_FOLDER = os.path.join('app', 'static', 'videos')
PROFILE_FOLDER = os.path.join('app', 'static', 'profiles')
os.makedirs(VIDEO_FOLDER, exist_ok=True)
os.makedirs(PROFILE_FOLDER, exist_ok=True)

@main.route('/')
def home():
    return render_template('index.html', user=current_user if current_user.is_authenticated else None)

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        if User.query.filter_by(email=email).first():
            flash('Email already registered.')
            return redirect(url_for('main.register'))

        if User.query.filter_by(username=username).first():
            flash('Username already taken.')
            return redirect(url_for('main.register'))

        new_user = User(username=username, email=email, role=role)
        new_user.password = password

        if role == 'viewer':
            new_user.coins = 20

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Registration successful!')
        return redirect(url_for('main.creator_dashboard' if role == 'creator' else 'main.viewer_dashboard'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('main.creator_dashboard' if user.role == 'creator' else 'main.viewer_dashboard'))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('main.login'))

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.home'))

@main.route('/creator')
@login_required
def creator_dashboard():
    if current_user.role != 'creator':
        return "Access denied", 403

    videos = Video.query.filter_by(creator_id=current_user.id).all()
    return render_template('creator_dashboard.html', user=current_user, videos=videos)

@main.route('/creator/setup', methods=['GET', 'POST'])
@login_required
def setup_channel():
    if current_user.role != 'creator':
        return "Access denied", 403

    if request.method == 'POST':
        current_user.channel_name = request.form['channel_name']
        current_user.category = request.form['category']

        profile = request.files.get('profile_picture')
        if profile:
            filename = secure_filename(profile.filename)
            filepath = os.path.join(PROFILE_FOLDER, filename)
            profile.save(filepath)
            current_user.profile_picture = filename

        db.session.commit()
        flash('Channel setup complete.')
        return redirect(url_for('main.creator_dashboard'))

    return render_template('creator_setup.html', user=current_user)

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_video():
    if current_user.role != 'creator':
        return "Access denied", 403

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        coin_cost = int(request.form['coin_cost'])
        file = request.files['video_file']

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(VIDEO_FOLDER, filename)
            file.save(filepath)

            video = Video(
                title=title,
                description=description,
                filename=filename,
                coin_cost=coin_cost,
                creator_id=current_user.id
            )
            db.session.add(video)
            db.session.commit()

            flash("Video uploaded successfully!")
            return redirect(url_for('main.creator_dashboard'))

    return render_template('upload_video.html', user=current_user)

@main.route('/viewer')
@login_required
def viewer_dashboard():
    if current_user.role != 'viewer':
        return "Access denied", 403

    videos = Video.query.all()
    unlocked_ids = [unlock.video_id for unlock in current_user.unlocked_videos]
    return render_template('viewer_dashboard.html', user=current_user, videos=videos, unlocked_ids=unlocked_ids)

@main.route('/unlock/<int:video_id>', methods=['POST'])
@login_required
def unlock_video(video_id):
    if current_user.role != 'viewer':
        return "Access denied", 403

    video = Video.query.get_or_404(video_id)

    already_unlocked = ViewerUnlock.query.filter_by(viewer_id=current_user.id, video_id=video.id).first()
    if already_unlocked:
        flash('You already unlocked this video.')
        return redirect(url_for('main.viewer_dashboard'))

    if current_user.coins < video.coin_cost:
        flash('Insufficient coins.')
        return redirect(url_for('main.viewer_dashboard'))

    current_user.coins -= video.coin_cost
    unlock = ViewerUnlock(viewer_id=current_user.id, video_id=video.id, coins_spent=video.coin_cost)
    db.session.add(unlock)
    db.session.commit()

    flash(f'Unlocked "{video.title}" successfully!')
    return redirect(url_for('main.viewer_dashboard'))

@main.route("/watch/<int:video_id>")
def watch_video(video_id):
    video = Video.query.get_or_404(video_id)
    creator = User.query.get(video.creator_id)
    return render_template("watch_video.html", video=video, creator=creator)

@main.route('/channel/<name>')
def view_channel(name):
    creator = User.query.filter(func.lower(User.channel_name) == func.lower(name)).first()
    if not creator:
        flash('Channel not found.')
        return redirect(url_for('main.viewer_dashboard'))

    videos = Video.query.filter_by(creator_id=creator.id).all()
    return render_template('view_channel.html', creator=creator, videos=videos, unlocked_ids=[
        unlock.video_id for unlock in current_user.unlocked_videos
    ] if current_user.is_authenticated and current_user.role == 'viewer' else [])

@main.route('/chat/codemaster', methods=['GET', 'POST'])
@login_required
def dummy_chat_codermaster():
    messages = [
        ("CodeMaster", "Hey! Ask me anything about coding."),
        ("You", "Hi! I want to learn Python."),
    ]

    if request.method == 'POST':
        new_msg = request.form.get('message')
        if new_msg:
            messages.append(("You", new_msg))

    now = datetime.now()
    return render_template('dummy_chat.html', messages=messages, creator_name="CodeMaster", now=now)
