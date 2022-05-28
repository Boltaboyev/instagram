from flask_migrate import *


SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/instagram_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
