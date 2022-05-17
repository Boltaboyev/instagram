import os

from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from models import *
from flask_migrate import *
import sys
from flask_script import Manager


SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost:5432/instagram_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
