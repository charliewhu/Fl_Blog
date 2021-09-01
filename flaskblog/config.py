import os
import dotenv


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class Config:
    
    dotenv_file = os.path.join(BASE_DIR, ".env")
    if os.path.isfile(dotenv_file):
        dotenv.load_dotenv(dotenv_file)

    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')\
        .replace('postgres://', 'postgresql://')\
        or 'sqlite:///' + \
        os.path.join(BASE_DIR, 'app.db')

    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_PORT = os.environ['MAIL_PORT']
    MAIL_USE_TLS = os.environ['MAIL_USE_TLS']
    MAIL_USERNAME = os.environ['MAIL_USERNAME']