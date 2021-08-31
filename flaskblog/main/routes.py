from flask import render_template, request, Blueprint, flash, redirect, url_for
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment, User
from flaskblog.posts.forms import CommentForm
from flaskblog.posts.utils import create_comment



main = Blueprint('main', __name__)


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    
    form = CommentForm()
    create_comment(form)

    return render_template('base/index.html', posts=posts, form=form)


@main.route("/about")
def about():
    return render_template('base/about.html', title='About')
