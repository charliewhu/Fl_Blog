from flask import Blueprint

main = Blueprint('main', __name__)

from flaskblog.main import routes