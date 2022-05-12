from flask import Flask
from config import *
from models import *
from flask_migrate import *
from flask_script import *

app = Flask(__name__)
app.config.from_object('config')
db = setup(app)


@app.route('/')
def hello_world():
    return "hello world"


manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == 'main':
    manager.run()