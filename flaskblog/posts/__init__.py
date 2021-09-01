from flask import Blueprint

posts = Blueprint('posts', __name__)

from flaskblog.posts import routes