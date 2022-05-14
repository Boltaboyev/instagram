from flask import Flask, flash

from config import *
from models import *
from flask_migrate import *
from flask_script import *
from config import *

# from werkzeug import

app = Flask(__name__)
app.config.from_object('config')
db = setup(app)
app.config['SECRET_KEY'] = 'dfjkdfohhdfiih'


def get_user():
    if "user" in session:
        username = Users.query.filter_by(name=session['user']).first()
        return username


@app.route('/')
def home():
    return render_template('home.html')




@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        request_pass = request.form.get('password')
        name = request.form.get('name')
        if len(request_pass) > 7:
            flash('Welcome to instagramm')
            gen_pass = generate_password_hash(request_pass, method='sha256')
            user_data = Users(name=name, password=gen_pass)
            db.session.add(user_data)
            db.session.commit()
            return redirect(url_for('register'))
        else:
            flash('Password must 8 character or more.')

    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    user = get_user()
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        get_user_name = Users.query.filter_by(name=name).first()
        if get_user_name:
            if check_password_hash(get_user_name.password, password):
                session['user'] = get_user_name.name
                print(session['user'])
                return redirect(url_for('home'))
            else:
                flash('wrong password.Please change your password !!!')
        else:
            flash('User name is not found !!!')
    return render_template('login.html', user=user)


@app.route('/follow')
def follow():
    return render_template('explore.html')


@app.route('/explore')
def explore():
    return render_template('explore.html')


@app.route('/user')
def user():
    return render_template('user.html')


manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == 'main':
    manager.run()
