from flaskblog.models import Post, Comment
from flask_login import current_user
from flask import flash, redirect, url_for
from flaskblog import db



def create_comment(form, redirect_url='main.home'):
    if form.validate_on_submit():
        post = Post.query.filter_by(id=form.postid.data).first()
        comment = Comment(text=form.text.data, user=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Comment created!', 'success')
        form.text.data = ''
        return redirect(url_for(redirect_url))