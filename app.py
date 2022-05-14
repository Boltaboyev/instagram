from flask import Flask, redirect, url_for, render_template
from flask_migrate import *
from flask_script import Manager
from models import *
from config import *

app = Flask(__name__)
db = setup(app)
app.config.from_object('config')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/follow')
def follow():
    return render_template('follow.html')


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
