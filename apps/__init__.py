# coding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from configs.config import AppConfig

db = SQLAlchemy()
login_manager = LoginManager()


def createApp():
    app = Flask(__name__)
    app.config.from_object(AppConfig)

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    from .user.view import user  # 不能放外面，否则会互相依赖
    app.register_blueprint(user, url_prefix='/user')
    return app
