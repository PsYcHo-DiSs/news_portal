from typing import Optional

from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column
from flask_login import UserMixin

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


class Users(db.Model, UserMixin):
    """Для профайла пользователя"""
    __tablename__ = 'users'
    id: int = db.Column(db.Integer, primary_key=True)
    username: str = db.Column(db.String(50), unique=True)
    first_name: str = db.Column(db.String(100))
    last_name: str = db.Column(db.String(100))
    phone: Optional[str] = db.Column(db.String(50), nullable=True)
    email: str = db.Column(db.String(100), unique=True)
    bio: Optional[str] = db.Column(db.String(300), nullable=True)
    photo: Optional[str] = db.Column(db.String(), nullable=True)
    password: str = db.Column(db.String(200))
    is_staff: bool = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.username
