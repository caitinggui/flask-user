# coding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPTokenAuth, HTTPBasicAuth, MultiAuth
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL

from utils import AppConfig

db = SQLAlchemy()
# 尽量不要用basic_auth和multi_auth,比较不安全
# 登陆的时候使用post验证，然后返回token，后续都使用token认证，需要更新token的时候就只用表单
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme='Bearer')
multi_auth = MultiAuth(basic_auth, token_auth)
app = Flask(__name__)
app.config.from_object(AppConfig)
db.init_app(app)
migrate = Migrate(app, db)
photos = UploadSet('photos', IMAGES)  # 'photos'就是flask-uploads set的名字
files = UploadSet('files', ALL)  # 路径是default加上set name


def createApp():
    configure_uploads(app, photos)
    configure_uploads(app, files)
    from .user.view import user  # 不能放外面，否则会互相依赖
    app.register_blueprint(user, url_prefix='/user')
    return app
