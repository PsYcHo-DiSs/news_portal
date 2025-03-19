from flask import Flask, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from dotenv import load_dotenv
import os

# Загружаем переменные окружения
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

# app.config['SQLALCHEMY_ECHO'] = True

app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['WTF_CSRF_ENABLED'] = os.getenv('WTF_CSRF_ENABLED') == "True"

# login_manager = LoginManager()
# login_manager.init_app(app)

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

