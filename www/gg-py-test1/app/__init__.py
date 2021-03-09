from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # app.config.from_pyfile('../config-extended.py')
    return app


app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
