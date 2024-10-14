from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from os import path
from flask_login import LoginManager
from datetime import date
import random


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///to_do_list.db'

    db.init_app(app)
    login_manager.init_app(app)

    from views import views
    from auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

    create_database(app)

    return app


def create_database(app):
    if not path.exists('instance/to_do_list.db'):
        with app.app_context():
            db.create_all()
        print('Created DataBase!!!')


@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))
