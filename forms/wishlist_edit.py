from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class WishlistEditForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    author = StringField("Автор", validators=[DataRequired()])
    submit = SubmitField('Применить')