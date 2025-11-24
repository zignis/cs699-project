from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=128)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=256)])
    submit = SubmitField('Login')
