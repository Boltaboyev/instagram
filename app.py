
from flask import Flask, redirect, url_for, render_template


from flask import Flask, redirect, url_for, render_template, flash


from config import *
from models import *

from flask_migrate import *
from flask_script import Manager
from models import *
from config import *

from werkzeug.utils import secure_filename


app = Flask(__name__)
db = setup(app)

app.config.from_object('config')

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



@app.route('/')
def home():
    user = get_current_user()
    return render_template('home.html', user=user)


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
        result = file_url+'/'+filename
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


@app.route('/follow')
def follow():
    return render_template('explore.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == 'main':
    manager.run()
