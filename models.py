from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
    name = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    data = db.relationship('User_data', backref="data_owner")


class User_data(db.Model):
    __tablename__ = 'user_data'
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.String())
    subscribers = db.relationship("Subscribers", backref='subscribers_owner')
    subscriptions = db.relationship('Subscriptions', backref='subscriptions_owner')
    posts = db.relationship("Posts", backref="posts_owner")
    user = db.Column(db.Integer, db.ForeignKey('users.id'))


class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String())
    post_owner = db.Column(db.Integer, db.ForeignKey('user_data.id'))
    post_like = db.relationship("Likes", backref="likes_owner")


class Subscribers(db.Model):
    __tablename__ = 'subscribers'
    id = db.Column(db.Integer, primary_key=True)
    subscriber_owner = db.Column(db.Integer, db.ForeignKey('user_data.id'))


class Likes(db.Model):
    __tablename__ = 'likes'
    id = db.Column(db.Integer, primary_key=True)
    like_owner = db.Column(db.Integer, db.ForeignKey('posts.id'))


class Subscriptions(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    subscription_owner = db.Column(db.Integer, db.ForeignKey('user_data.id'))
