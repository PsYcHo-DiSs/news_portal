from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:123456@127.0.0.1/news"
# app.config['SQLALCHEMY_ECHO'] = True

UPLOAD_FOLDER = 'news/static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SECRET_KEY'] = '555_777'
app.config['WTF_CSRF_ENABLED'] = True

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

