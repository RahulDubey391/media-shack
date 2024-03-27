# Form Based Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo, URL
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired

# User Based Imports
from flask_login import current_user
from src.models import User



class AddContentForm(FlaskForm):
    content_id = StringField('Content ID', validators=[DataRequired()])
    content_title = StringField('Content Title', validators=[DataRequired()])
    thumbnail = FileField('Thumbnail Image', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    video_url = StringField('Video URL', validators=[DataRequired(), URL()])
    submit = SubmitField('Add Content')