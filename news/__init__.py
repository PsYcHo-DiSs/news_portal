from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

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

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)
