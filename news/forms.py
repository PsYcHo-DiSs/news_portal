from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField, SelectField, FileField


class PostForm(FlaskForm):
    title = StringField('Заголовок статьи:')
    content = TextAreaField('Содержимое статьи:', render_kw={'rows': 15})
    category = SelectField('Категория:', choices=[])
    picture = FileField('Картинка для статьи')
