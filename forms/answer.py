from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class AnswerForm(FlaskForm):
    body = TextAreaField('Your answer', validators=[DataRequired(), Length(max=8192)])
    submit = SubmitField('Submit answer')
