from flask import Blueprint

accounts = Blueprint('accounts', __name__)

from flaskblog.accounts import routes