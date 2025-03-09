from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# create the extension
db = SQLAlchemy()

# create the app
app = Flask(__name__)

# configure the Postgres database
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://postgres:123456@127.0.0.1/news"

# initialize the app with the extension
db.init_app(app)

# Create Model
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column


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

    def __repr__(self):
        return self.title


@app.route('/')
@app.route('/index')
def index():
    """Главная страница"""
    posts = Post.query.all()
    categories = Category.query.all()
    return render_template('news/index.html',
                           title='Главная',
                           categories=categories,
                           posts=posts)


@app.route('/category/<int:id>')
def category_list(id: int):
    """Возврат ответа на нажатие кнопок категорий"""
    # все имеющиеся категории
    categories = Category.query.all()
    # фильтруем имеющиеся посты согласно подставляемому id
    posts = Post.query.filter(Post.category_id == id)
    # current это название категории (которая уходит в тайтл тэг)
    current = Category.query.get(id)
    return render_template('news/index.html',
                           title=current,
                           categories=categories,
                           posts=posts,
                           current=current)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.160', port=8000)
