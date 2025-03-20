from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, SelectField, FileField
from wtforms import PasswordField, validators


class PostForm(FlaskForm):
    """Форма для заполния поста"""
    title = StringField('Заголовок статьи:')
    content = TextAreaField('Содержимое статьи:', render_kw={'rows': 15})
    category = SelectField('Категория:', choices=[])
    picture = FileField('Картинка для статьи')


class Registration(FlaskForm):
    """Форма для регистрации пользователя"""
    username = StringField('Логин: *', [validators.DataRequired()])
    first_name = StringField('Имя: *', [validators.DataRequired()])
    last_name = StringField('Фамилия: *', [validators.DataRequired()])
    phone = StringField('Контактный телефон:')
    email = StringField('Почта: *', [validators.DataRequired()])
    password = PasswordField('Пароль: *', [validators.Length(min=1, max=15),
                                           validators.EqualTo('confirm',
                                                              message='Пароли должны совпадать!')])
    confirm = PasswordField('Подтверждение пароля: *', [validators.DataRequired()])


class UserLogin(FlaskForm):
    """Форма для авторизации пользователя"""
    username = StringField('Логин')
    password = PasswordField('Пароль')


class UpdateUserProfile(FlaskForm):
    """Форма для редактирования профайла пользователя"""
    username = StringField("Логин: *", [validators.DataRequired()])
    first_name = StringField('Имя: *', [validators.DataRequired()])
    last_name = StringField('Фамилия: *', [validators.DataRequired()])
    phone = StringField('Контактный телефон:')
    email = StringField('Почта: *', [validators.DataRequired()])
    bio = TextAreaField('БИО:', render_kw={'rows': 5})
    photo = FileField('Аватарка')
