from typing import Optional, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired, Optional


class CommentForm(FlaskForm):
    text    = StringField('text', validators=[DataRequired()], render_kw={"placeholder": "Comment"})
    postid  = HiddenField('postid', validators=[Optional()])
    submit  = SubmitField('Post')
