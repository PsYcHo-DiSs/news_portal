import os
import uuid as uuid

from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from flask import render_template, request, abort, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from news import db, app
from news.forms import PostForm
from news.models import Post, Category
from news.forms import Registration, UpdateUserProfile
from news.models import Users
from news.forms import UserLogin

# Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user_login'


@login_manager.user_loader
def load_user(user_id):
    """Чекер пользователя, по документации"""
    return db.session.get(Users, int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    """Аутентификация пользователя"""
    form = UserLogin()
    if request.method == 'POST':
        user = Users.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Вы успешно вошли в систему", "success")
            return redirect(url_for('index'))
        else:
            flash("Неверный логин или пароль", "error")

    return render_template('news/user_login.html', form=form)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration', methods=['POST', 'GET'])
def user_registration():
    form = Registration()
    if request.method == 'POST' and form.validate():
        password_hash = generate_password_hash(form.password.data, method='scrypt')
        user = Users(first_name=form.first_name.data,
                     last_name=form.last_name.data,
                     username=form.username.data,
                     phone=form.phone.data,
                     email=form.email.data,
                     password=password_hash)
        try:
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            flash("Аккаунт успешно создан, пожалуйста, войдите в учётную запись!")
            return redirect(url_for('user_login'))
        except IntegrityError:
            db.session.rollback()
            flash("Пользователь с такими данными существует!", "error")

    return render_template('news/user_registration.html', form=form)


@app.route('/profile/<int:id>')
@login_required
def user_profile(id: int):
    """Профайл пользователя"""
    user = db.session.get(Users, id)
    if not user:
        flash("Пользователя с таким id не существует", "error")
        return redirect(url_for('index'))
    return render_template('news/user_profile.html', user=user)


@app.route('/profile/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id: int):
    """Удаление пользователя"""
    user_to_delete = db.session.get(Users, id)
    if not user_to_delete:
        flash("Пользователь не найден или уже удалён", "error")
        abort(404)
    if current_user.id != user_to_delete.id:
        flash("Вы не имеете таких полномочий", "error")
        abort(403)
    db.session.delete(user_to_delete)
    db.session.commit()
    flash(f"Профайл {user_to_delete.username} успешно удалён!", 'success')

    return redirect(url_for('index'))


@app.route('/profile/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update_user(id: int):
    """Логика для редактирования пользователя"""
    user = db.session.get(Users, id)
    form = UpdateUserProfile(obj=user)
    if current_user.id != user.id:
        flash("Вы не имеете таких полномочий", "error")
        abort(403)
    if request.method == 'POST':
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.phone = form.phone.data
        user.email = form.email.data
        user.bio = form.bio.data

        avatar_file = form.photo.data
        if avatar_file:
            avatar_name = secure_filename(avatar_file.filename)
            avatar_name = str(uuid.uuid4()) + '_' + avatar_name
            avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], avatar_name)

            avatar_file.save(avatar_path)
            user.photo = avatar_name

        try:
            db.session.add(user)
            db.session.commit()
            flash("Информация о пользователе успешно отредактирована!", "success")
            return redirect(url_for('user_profile', id=user.id))
        except IntegrityError:
            db.session.rollback()
            flash("Пользователь с такими данными существует!", "error")

    return render_template('news/edit_user_profile.html', form=form, id=id)


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
    # current = Category.query.get(id)  # легаси код для 1.4
    current = db.session.get(Category, id)  # новый аналог
    return render_template('news/index.html',
                           title=current,
                           categories=categories,
                           posts=posts,
                           current=current)


@app.route('/post/<int:id>')
def post_detail(id: int):
    """Статья на отдельной странице"""
    # post = Post.query.get(id) # более старый вариант
    # post = db.session.execute(db.select(Post).filter_by(id=id)).scalar()
    # post = db.session.get(Post, id)
    post = Post.query.filter(Post.id == id).first()
    return render_template('news/post_detail.html', post=post)


@app.route('/search/', methods=['GET'])
def search_result():
    """Функционал для поиска"""
    q = request.args.get('q')
    categories = Category.query.all()
    # search = Post.title.contains(q) | Post.content.contains(q)
    search = (Post.title.ilike(f'%{q}%') | Post.content.ilike(f'%{q}%'))
    posts = Post.query.filter(search).all()

    if posts:
        flash("Информация найдена в системе!", 'success')
    else:
        flash("Искомой информации не найдено!", "error")
        abort(404)
    return render_template('news/index.html',
                           categories=categories,
                           posts=posts)


@app.errorhandler(404)
def page404(e):
    return render_template('news/404.html'), 404


@app.errorhandler(403)
def page403(e):
    return render_template('news/403.html'), 403


@app.route('/post/create', methods=['POST', 'GET'])
@login_required
def create_post():
    form = PostForm()
    form.category.choices = [c.title for c in Category.query.all()]
    # Логика обработки запроса
    if request.method == 'POST':
        category_id = Category.query.filter_by(title=form.category.data).first().id

        picture_file = form.picture.data

        picture_name = None  # По умолчанию пустое значение
        if picture_file:
            picture_name = secure_filename(picture_file.filename)
            picture_name = str(uuid.uuid4()) + '_' + picture_name
            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_name)

            # Сохраняем сам файл
            picture_file.save(picture_path)

        post = Post(title=form.title.data,
                    content=form.content.data,
                    category_id=category_id,
                    picture=picture_name)

        db.session.add(post)
        db.session.commit()
        flash(f"Статья {form.title.data} успешно создана!", "success")
        return redirect(url_for('category_list', id=category_id))

    # # Отправка данных для отображения формы
    return render_template('news/create_post.html', form=form)


@app.route('/post/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id: int):
    """Удаление поста"""
    post_to_delete = db.session.get(Post, id)
    if not post_to_delete:
        flash("Пост не найден или уже удалён", "error")
        abort(404)

    category_id = post_to_delete.category_id
    db.session.delete(post_to_delete)
    db.session.commit()
    flash(f"Статья {post_to_delete.title} успешно удалена!")

    return redirect(url_for('category_list', id=category_id))


@app.route('/post/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update_post(id: int):
    """Функция редактирования поста"""
    post = db.session.get(Post, id)
    form = PostForm(obj=post)
    form.category.choices = [c.title for c in Category.query.all()]

    if request.method == 'POST':
        category_id = Category.query.filter_by(title=form.category.data).first().id
        post.category_id = category_id
        post.title = form.title.data
        post.content = form.content.data

        picture_file = form.picture.data
        if picture_file:
            picture_name = secure_filename(picture_file.filename)
            picture_name = str(uuid.uuid4()) + '_' + picture_name
            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], picture_name)

            picture_file.save(picture_path)
            post.picture = picture_name

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post_detail', id=id))

    return render_template('news/create_post.html', form=form, id=id)


# Utils
@app.template_filter('time_filter')
def jinja2_filter_datetime(date):
    format_type = '%d.%m.%Y %H:%M:%S'
    return date.strftime(format_type)
