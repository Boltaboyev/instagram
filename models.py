import datetime
from time import timezone
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func

db = SQLAlchemy()


def setup(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    email = db.Column(db.String())
    password = db.Column(db.String())
    img = db.Column(db.String(), nullable=True)
    subscriptions = db.relationship(
        'Subscriptions', backref='subscriptions_owner', foreign_keys='Subscriptions.subscriptions_owner2')
    subscribers = db.relationship(
        'Subscriptions', backref='subscribers_owner', foreign_keys='Subscriptions.subscribers_owner2')
    posts = db.relationship(
        "Posts", backref="posts_owner", order_by='Posts.id')
    comments = db.relationship(
        "Comments", backref="comments_owner", order_by='Comments.id')


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post_img = db.Column(db.String())
    post_comment = db.Column(db.String())
    post_owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_like = db.relationship(
        "Likes", backref="likes_owner", order_by="Likes.id")
    post_head = db.Column(db.Boolean())
    post_comments = db.relationship(
        "Comments", backref="comments_owner_post", order_by="Comments.id")
    like_count = db.Column(db.Integer)
    comment_count = db.Column(db.Integer)
    created = db.Column(
        db.DateTime(timezone=True), default=func.now(), nullable=True)


class Likes(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    like_owner = db.Column(db.Integer, db.ForeignKey('posts.id'))


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment_owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    comment_text = db.Column(db.String())
    created_at = db.Column(
        db.DateTime(timezone=True), default=func.now(), nullable=True)


class Subscriptions(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer)
    subscriptions_owner2 = db.Column(db.Integer, db.ForeignKey('users.id'))
    subscribers_owner2 = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(
        db.DateTime(timezone=True), default=func.now(), nullable=True)
