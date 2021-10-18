from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


''' The model for the database tables '''


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # Prints objects of this class for debugging purposes
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # function to generate a password hash
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # function to check password hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# this is used for logging in the user given their ID
@login.user_loader
def loader_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(64))
    title = db.Column(db.String(128))
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    # Prints objects of this class for debugging purposes
    def __repr__(self):
        return '<Post {}>'.format(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    replies = db.relationship(
            'Comment', backref=db.backref('parent', remote_side=[id]),
            lazy='dynamic')

    # Prints objects of this class for debugging purposes
    def __repr__(self):
        return '<Comment {}>'.format(self.description)
