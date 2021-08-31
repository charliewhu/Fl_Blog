from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id          = db.Column(db.Integer, primary_key=True)
    username    = db.Column(db.String(20), unique=True, nullable=False)
    email       = db.Column(db.String(120), unique=True, nullable=False)
    image_file  = db.Column(db.String(20), nullable=False, default='default.jpg')
    password    = db.Column(db.String(60), nullable=False)
    updated_on  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    posts       = db.relationship('Post', backref='author', lazy=True, cascade='all, delete, delete-orphan')
    comments    = db.relationship('Comment', backref='user', cascade='all, delete, delete-orphan')
    likes       = db.relationship('Like', backref='user', cascade='all, delete, delete-orphan')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    title       = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated= db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    content     = db.Column(db.Text, nullable=False)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    comments    = db.relationship('Comment', backref='post', cascade='all, delete, delete-orphan')
    likes       = db.relationship('Like', backref='post', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    text        = db.Column(db.String(200), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id     = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)


class Like(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    date_created= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id     = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id     = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)


