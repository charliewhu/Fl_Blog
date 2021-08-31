from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title   = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit  = SubmitField('Post')


class CommentForm(FlaskForm):
    text    = StringField('text', validators=[DataRequired()], render_kw={"placeholder": "Add Comment Here.."})
    postid  = HiddenField('postid', validators=[DataRequired()])
    submit  = SubmitField('Post')