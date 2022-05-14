import os

SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/instagram_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
