from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column

from news import db


class Category(db.Model):
    """Категории постов"""
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    posts = db.relationship('Post', back_populates='category')

    def __repr__(self):
        return self.title


class Post(db.Model):
    """Новостные посты"""
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())
    category_id = mapped_column(ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')
    picture = db.Column(db.String(), nullable=True)

    def __repr__(self):
        return self.title


class Users(db.Model):
    """Для профайла пользователя"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), unique=True)
    bio = db.Column(db.String(300), nullable=True)
    photo = db.Column(db.String(), nullable=True)
    password = db.Column(db.String(150))
    is_staff = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.username
