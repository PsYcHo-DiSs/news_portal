import os
import uuid as uuid
from werkzeug.utils import secure_filename

from flask_admin import Admin, AdminIndexView
from flask_login import current_user
from flask import redirect, url_for, flash
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField

from news import app, db
from news.models import Category, Post, Users


def prefix_name(obj, file_data):
    """Преобразование имени файла, приведение к уникальности"""
    parts = os.path.splitext(file_data.filename)
    return secure_filename(f'{uuid.uuid4()}_%s%s' % parts)


class AdminAccess(AdminIndexView):
    def is_accessible(self):
        """Логика доступности для конкретного пользователя"""
        if not current_user.is_anonymous:
            return current_user.is_staff

    def inaccessible_callback(self, name, **kwargs):
        """Срабатывает, если у пользователя нет доступа"""
        flash("У вас нет полномочий для входа в админ панель!", "error")
        return redirect(url_for('index'))


class PostAdmin(ModelView):
    form_columns = ['title', 'content', 'category', 'picture', 'author_id']

    form_extra_fields = {
        'picture': FileUploadField('picture',
                                   base_path=app.config['UPLOAD_FOLDER'],
                                   namegen=prefix_name),
    }


class UsersAdmin(ModelView):
    form_columns = ['username', 'first_name', 'last_name', 'phone', 'email',
                    'bio', 'photo', 'password', 'is_staff']

    form_extra_fields = {
        'photo': FileUploadField('photo',
                                 base_path=app.config['UPLOAD_FOLDER'],
                                 namegen=prefix_name),
    }


admin = Admin(app, template_mode='bootstrap4', index_view=AdminAccess())
admin.add_view(ModelView(Category, db.session))
admin.add_view(PostAdmin(Post, db.session))
admin.add_view(UsersAdmin(Users, db.session))
# models = (Category, Post, Users)
#
# for cls in models:
#     admin.add_view(ModelView(cls, db.session))
