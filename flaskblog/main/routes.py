from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment, User
from .forms import CommentForm


main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    form = CommentForm()
    if form.validate_on_submit():
        post = Post.query.filter_by(id=form.postid.data).first()
        comment = Comment(text=form.text.data, user=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Comment created!', 'success')
        return redirect(url_for('main.home'))

    return render_template('base/index.html', posts=posts, form=form)


@main.route("/about")
def about():
    return render_template('base/about.html', title='About')
