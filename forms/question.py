from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class QuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=256)])
    body = TextAreaField('Body', validators=[DataRequired(), Length(max=8192)])
    tags = StringField('Tags (comma separated)')
    submit = SubmitField('Post question')
