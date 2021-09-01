from flaskblog import create_app, db
from flaskblog.models import User, Post

app = create_app()





@app.shell_context_processor
def make_shell_context():
    """loads packages into flask shell"""
    return {'db': db, 'User': User, 'Post': Post}