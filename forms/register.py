from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp, ValidationError

class RegisterForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=48),
            Regexp(r'^[a-zA-Z0-9_]+$', message="Username contains invalid characters")
        ]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            Length(max=128)
        ]
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=256)]
    )

    confirm_password = PasswordField(
        'Confirm password',
        validators=[DataRequired(), EqualTo('password')]
    )

    submit = SubmitField('Register')

   
    def validate_email(self, field):
        email = (field.data or '').strip().lower()

    
        if not email.endswith('@iitb.ac.in'):
            raise ValidationError('Please register with Institute email address')

      
        from models import User
        if User.query.filter_by(email=email).first():
            raise ValidationError('This email is already registered.')
