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
from app.models import User, Account

db.create_all()


def filling_db():
    # First run db filling
    if not User.query.filter_by(username='admin').first():
        user = User(username='admin', email='email@mail.no')
        user.set_password('admin')
        db.session.add(user)
        db.session.commit()
        for i in range(11):
            account = Account(nickname='Account'+str(i), rank=i, clanname='ClanTest', accounttype=1)
            db.session.add(account)
            db.session.commit()


filling_db()
