
from datetime import timedelta
from turtle import pos
from urllib import request

from flask import Flask, redirect, url_for, render_template, session, request, jsonify
import re
from flask import Flask, redirect, url_for, render_template
from flask import Flask, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash, generate_password_hash


from config import *
from models import *

from flask_migrate import *
from flask_script import Manager
from models import *
from config import *

from werkzeug.utils import secure_filename

from werkzeug.utils import secure_filename


app = Flask(__name__)
db = setup(app)
app.config['SECRET_KEY'] = 'dfjkdfohhdfiih'


def get_user():
    if "user" in session:
        username = Users.query.filter_by(name=session['user']).first()
        return username


def get_current_user():
    user_query = None
    if 'user' in session:
        user = session['user']
        user = Users.query.filter_by(username=user).first()
        user_query = user
    return user_query


app.config.from_object('config')

app.config['SECRET_KEY'] = 'dfjkdfohhdfiih'


def get_current_user():
    user_query = None
    if 'user' in session:
        user = session['user']
        user = Users.query.filter_by(username=user).first()
        user_query = user
    return user_query


@app.route('/')
def home():
    user = get_current_user()
    followed_users = []
    if user:
        users = Users.query.filter(Users.id != user.id).all()
        owner = Subscriptions.query.filter_by(
            subscribers_owner2=user.id).all()
        owner_get = Subscriptions.query.filter(
            Subscriptions.subscribers_owner2 == user.id).all()
        posts = Posts.query.all()
        for item in owner_get:
            followed_users.append(item.owner_id)
        followed_users.append(user.id)
        suggested_users = Users.query.filter(~Users.id.in_(
            [user_id for user_id in followed_users])).all()
        print(suggested_users)
        return render_template('home.html', owner_get=owner_get, user=user, users=users, owner=owner, posts=posts, suggested_users=suggested_users)
    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        get_user = Users.query.filter_by(username=name).first()
        if get_user:
            if check_password_hash(get_user.password, password):
                session['user'] = get_user.username
                return redirect(url_for('home'))
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('re-password')
        photo = request.files['image_user']
        filename = secure_filename(photo.filename)
        photo.save(os.path.join("static/img/person", filename))
        file_url = "static/img/person"

        result = file_url + '/' + filename

        if len(email) <= 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(username) <= 2:
            flash(
                'Username must be greater than 2 characters', category='error')
        elif len(password) <= 4:
            flash('Password must be greater than 4 characters', category='error')
        elif password != password2:
            flash('Password do not match', category='error')
        else:
            new_user = Users(email=email, username=username,
                             password=generate_password_hash(password, method='sha256'), img=result)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created', category='success')

            get_user = Users.query.filter_by(username=username).first()
            session['user'] = get_user.username
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/subscribings/<int:user_id>')
def subscriber(user_id):
    user = get_current_user()
    user2 = Users.query.filter_by(id=user_id).first()
    users = Users.query.all()
    subscrings = Subscriptions.query.filter_by(
        subscribers_owner2=user.id).all()
    return render_template('follow.html', users=users, user=user, subscrings=subscrings, user2=user2)


@app.route('/subscribers/<int:user_id>')
def subscribers(user_id):
    user = get_current_user()
    user2 = Users.query.filter_by(id=user_id).first()
    users = Users.query.all()
    owner = Subscriptions.query.filter_by(
        subscriptions_owner2=user.id).all()
    return render_template('followers.html', user=user, users=users, owner=owner, user2=user2)


@app.route('/follow/<int:subscribed_id>')
def follow(subscribed_id):
    user = get_current_user()
    follow = Subscriptions(owner_id=user.id,
                           subscriptions_owner2=subscribed_id)
    be_followed = Subscriptions(owner_id=subscribed_id,
                                subscribers_owner2=user.id)
    db.session.add(follow)
    db.session.add(be_followed)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    object = {}
    object['like'] = 'False'
    current_user = get_current_user()
    like = Likes(owner_id=current_user.id,
                 like_owner=post_id)
    like2 = Likes.query.filter_by(owner_id=current_user.id,
                                  like_owner=post_id).first()
    post = Posts.query.filter_by(id=post_id).first()
    complete = request.get_json()['liked']
    if like2:
        # post.post+like.remove()
        db.session.delete(like2)
        object['like'] = 'False'
        complete = 'true'
    else:
        object['like'] = 'True'
        db.session.add(like)

        complete = 'false'
    db.session.commit()
    likes = Likes.query.filter_by(like_owner=post_id).all()
    count_likes = len(likes)
    numb_likes = len(post.post_like)
    Posts.query.filter_by(id=post_id).update({"like_count": numb_likes})
    db.session.commit()
    object['count'] = numb_likes
    lik3 = Likes.query.filter_by(owner_id=current_user.id,
                                 like_owner=post_id).first()
    return jsonify(object)


@app.route('/get_post/<int:post_id>', methods=['POST', 'GET'])
def get_post(post_id):
    object = {}
    comment_list = []
    post_open = Posts.query.filter_by(id=post_id).first()
    comments = Comments.query.filter_by(comment_post_id=post_id).all()

    for comment in comments:
        comment_dict = {}
        comment_differ_str = ''
        comment_dict['owner_username'] = comment.comments_owner.username
        comment_dict['owner_img'] = comment.comments_owner.img
        comment_dict['comment_text'] = comment.comment_text
        comment_dict['commented_at'] = comment.created_at
        comment_dict['now'] = datetime.datetime.now()

        comment_differ = datetime.datetime.now() - comment.created_at
        if comment_differ < timedelta(minutes=60):
            comment_differ_str = str(
                int(comment_differ.total_seconds()/60)) + 'm'
        elif comment_differ < timedelta(hours=24):
            comment_differ_str = str(
                int(comment_differ.total_seconds()/3600)) + 'h'
        elif comment_differ < timedelta(days=30):
            comment_differ_str = str(
                int(comment_differ.total_seconds()/86400)) + 'd'
        else:
            comment_differ_str = 'a long time'
        comment_dict['comment_differ_str'] = comment_differ_str
        # comment_dict['commented_ago'] = comment_differ
        comment_list.append(comment_dict)
    # post_open_owner = Posts.query.filter_by(id=post_id).first().

    users = Users.query.all()
    object['post_open_id'] = post_open.id
    object['post_open_img'] = post_open.post_img
    object['post_open_owner'] = post_open.post_owner
    object['post_open_owner_img'] = post_open.posts_owner.img
    object['post_open_owner_username'] = post_open.posts_owner.username
    object['post_open_like_count'] = post_open.like_count
    object['comment_list'] = comment_list
    if post_open.created:
        post_differ = datetime.datetime.now() - post_open.created
        post_differ_str = ''
        if post_differ < timedelta(minutes=60):
            post_differ_str = str(
                int(post_differ.total_seconds()/60)) + 'm'
        elif post_differ < timedelta(hours=24):
            post_differ_str = str(
                int(post_differ.total_seconds()/3600)) + 'h'
        elif post_differ < timedelta(days=30):
            post_differ_str = str(
                int(post_differ.total_seconds()/86400)) + 'd'
        else:
            post_differ_str = 'a long time'
        object['post_differ_str'] = post_differ_str
        object['post_open_date'] = post_open.created
    post_open.posts_owner.img
    # object['users'] = users

    user = get_current_user()
    return jsonify(object)


@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    user = get_current_user()
    object = {}
    users = Users.query.all()
    comment_text = request.get_json()['comment_text']
    new_comment = Comments(
        comment_owner_id=user.id, comment_post_id=post_id, comment_text=comment_text)
    db.session.add(new_comment)
    db.session.commit()
    comment = Comments.query.filter_by(comment_post_id=post_id).first()
    object['owner_username'] = user.username
    object['owner_img'] = user.img
    object['comment_text'] = comment_text
    post = Posts.query.filter_by(id=post_id).first()
    numb_comments = len(post.post_comments)
    Posts.query.filter_by(id=post_id).update({"comment_count": numb_comments})
    db.session.commit()
    return jsonify(object)
    # comment_text = request.form.get('comment_text')
    # date_now = datetime.datetime.now()
    # post_open = Posts.query.filter_by(id=post_id).first()
    # if request.method == 'POST':
    #     new_comment = Comments(
    #         comment_owner_id=user.id, comment_post_id=post_id, comment_text=comment_text, created_at=date_now)
    #     db.session.add(new_comment)
    #     db.session.commit()
    #     return redirect(url_for('get_post', post_id=post_id))


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/user', methods=["POST", "GET"])
def user():
    current_user = get_current_user()
    posts = Posts.query.filter_by(post_owner=current_user.id).all()
    user = Users.query.filter_by(id=current_user.id).first()
    if request.method == "POST":
        photo = request.files['update']
        get_userId = Users.query.filter_by(id=user.id).first()

        if os.path.exists(get_userId.img):
            os.remove(get_userId.img)

        filename = secure_filename(photo.filename)
        photo.save(os.path.join("static/img/person", filename))
        file_url = "static/img/person"
        result = file_url+'/'+filename
        Users.query.filter_by(id=user.id).update({"img": result})
        db.session.commit()
        return redirect(url_for('user', user=user))
    return render_template('user.html', user=user, posts=posts, current_user=current_user)


@app.route('/view_user/<int:user_id>', methods=["POST", "GET"])
def view_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    current_user = get_current_user()
    posts = Posts.query.filter_by(post_owner=user.id).all()
    subs = Subscriptions.query.filter_by(
        owner_id=current_user.id, subscriptions_owner2=user.id).first()
    return render_template('user.html', user=user, posts=posts, current_user=current_user, subs=subs)


@app.route('/suggested_users')
def suggested_users():
    users = Users.query.all()
    current_user = get_current_user()

    subs = Subscriptions.query.filter_by(owner_id=current_user.id).all()
    return render_template('suggested_users.html', users=users, current_user=current_user, subs=subs, user=user)


@app.route('/remove_img')
def remove_img():
    user = get_current_user()
    dele_img = Users.query.filter_by(id=user.id).first()
    dele_img.img = ""
    db.session.commit()

    return redirect(url_for("user"), user=user)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/posts', methods=["POST", 'GET'])
def add_post():
    user = get_current_user()

    if request.method == 'POST':
        comment = request.form.get("comment")
        photo = request.files['post']
        filename = secure_filename(photo.filename)
        photo.save(os.path.join("static/img/person", filename))
        file_url = "static/img/person"

        result = file_url + '/' + filename

        add = Posts(post_img=result, post_owner=user.id, post_comment=comment)
        db.session.add(add)
        db.session.commit()
    return redirect(url_for("user"))


@app.route('/hide')
def hide_acaunt():
    current_user = get_current_user()
    get_user = Users.query.filter_by(id=current_user.id).first()
    if get_user.post_type:
        get_user.post_type = False
        db.session.commit()
    else:
        get_user.post_type = True
        db.session.commit()
    return redirect(url_for('user'))


manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == 'main':
    manager.run()
