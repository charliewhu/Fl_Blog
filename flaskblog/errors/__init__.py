from flask import Blueprint

errors = Blueprint('errors', __name__)

from flaskblog.errors import handlers