from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp
from flask_wtf.file import FileAllowed

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=48), Regexp(r'^[a-zA-Z0-9_]+$', message="Username contains invalid characters" )])
    avatar = FileField('Avatar', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    remove_avatar = BooleanField('Remove current avatar')
    current_password = PasswordField('Current password')
    new_password = PasswordField('New password', validators=[Length(max=256)])
    confirm_password = PasswordField('Confirm password', validators=[EqualTo('new_password')])
    submit = SubmitField('Save changes')
