from src import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False) 

    # This connects BlogPosts to a User Author.
    posts = db.relationship('MediaPost', backref='author', lazy=True)

    def __init__(self, email, username, password,  is_admin=False):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"


class MediaPost(db.Model):
    __tablename__ = 'mediaposts'

    users = db.relationship(User)

    content_id = db.Column(db.String(20), primary_key=True)  # Using content_id as the primary key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content_title = db.Column(db.String(100), nullable=False)
    thumbnail_url = db.Column(db.String(100), nullable=False)  # Store relative path to thumbnail
    video_url = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, content_id, user_id, content_title, thumbnail_url, video_url):
        self.content_id = content_id
        self.user_id = user_id
        self.content_title = content_title
        self.thumbnail_url = thumbnail_url
        self.video_url = video_url

    def __repr__(self):
        return f"MediaPost: {self.content_title}"