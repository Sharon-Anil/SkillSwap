from datetime import datetime
from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    channel_name = db.Column(db.String(150), unique=True)
    profile_picture = db.Column(db.String(255), default='default_profile.jpg')
    thumbnail = db.Column(db.String(255))
    category = db.Column(db.String(100))
    bio = db.Column(db.Text)
    social_links = db.Column(db.JSON)

    coins = db.Column(db.Integer, default=20)
    watch_history = db.relationship('WatchHistory', backref='user', lazy=True)

    videos = db.relationship('Video', backref='creator', lazy=True, cascade='all, delete-orphan')
    unlocked_videos = db.relationship('ViewerUnlock', backref='viewer', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can_unlock(self, video):
        return self.coins >= video.coin_cost if video.coin_cost > 0 else True

    def has_unlocked(self, video):
        return any(u.video_id == video.id for u in self.unlocked_videos)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    thumbnail = db.Column(db.String(255), default='default_thumbnail.jpg')
    coin_cost = db.Column(db.Integer, nullable=False, default=0)
    duration = db.Column(db.Integer)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean, default=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    viewer_unlocks = db.relationship('ViewerUnlock', backref='video', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='video', lazy=True, cascade='all, delete-orphan')
    watch_history = db.relationship('WatchHistory', backref='video', lazy=True)

    def increment_views(self):
        self.views += 1
        db.session.commit()

class ViewerUnlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    viewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)
    coins_spent = db.Column(db.Integer, nullable=False, default=0)

    __table_args__ = (db.UniqueConstraint('viewer_id', 'video_id', name='unique_unlock'),)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)

class WatchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    watched_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Boolean, default=False)

    __table_args__ = (db.UniqueConstraint('user_id', 'video_id', name='unique_watch_history'),)
