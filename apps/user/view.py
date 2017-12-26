# coding: utf-8
"""
permission_required装饰器要在login_required下面
login时自己处理表单，不要用basic_auth，这里仅是演示
后面的登陆验证只允许用token_auth!!!
"""
import logging
import os

from flask import Blueprint, request, g, send_file
from flask_uploads import UploadNotAllowed

from .. import db, basic_auth, token_auth, multi_auth, photos, files
from ..models import User, Permission
from utils import requestGetParam, requestPostParam, RetCode, webJson, permission_required, Constant


user = Blueprint('user', __name__)
logger = logging.getLogger(__name__)


def saveAvatar(user, img):
    """根据Email生成头像的路径和文件名"""
    if len(img.read()) > Constant.avatar_max_size:
        logger.warn("avatar too big")
        raise(ValueError)
    suffix = img.filename.split('.')[-1]
    filename = '{}.{}'.format(hash(user.email), suffix)
    folder = str(user.id % Constant.avatar_folder_size)  # 一个目录下的文件过多会影响读文件效率
    folder = os.path.join(Constant.avatar_basedir, folder)
    filename = photos.save(img, folder=folder, name=filename)
    logger.info("avatar name: %s", filename)
    return filename


@user.route("/regist", methods=["POST"])
def regist():
    email = requestPostParam(request, 'email')
    password = requestPostParam(request, 'password')
    img = request.files.get("img", None)
    logger.info("email: %s, img: %s", email, img)
    if None in (email, password, img):
        return webJson(RetCode.PARAMS_ERROR)
    if User.query.filter_by(email=email).first():
        logger.warn('email duplication')
        return webJson(RetCode.EMAIL_DUPLICATION)

    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    try:
        avatar = saveAvatar(user, img)
    except UploadNotAllowed:
        return webJson(RetCode.FILE_SUFFIX_ERROR)
    except ValueError:
        return webJson(RetCode.AVATAR_TOO_BIG)
    user.avatar = avatar
    db.session.add(user)
    db.session.commit()
    return webJson(RetCode.SUCCESS)


@user.route('/login', methods=['GET', 'POST'])
@basic_auth.login_required
def login():
    """获取token只允许用账号和密码，禁止用token更新token.
    这里最好不用login_required，而是自己处理一个表单，
    然后把token返回去，后续再使用token_auth"""
    user_info = g.user.info()
    user_info["token"] = g.user.generate_auth_token()
    return webJson(RetCode.SUCCESS, data=user_info)


@user.route('/test_login')
@multi_auth.login_required
def test():
    """用账户密码或者token都可以"""
    if g.user:
        return '<h1>you are still in</h1>'
    else:
        return '<h1>you have logouted</h1>'


@user.route('/test_permission')
@multi_auth.login_required
@permission_required(Permission.DOWNLOAD)
def testPermission():
    return 'your rights ard OK'


@user.route('/upload', methods=["POST"])
def test_upload():
    upload_file = request.files.get("files", None)
    logger.info('---%s', upload_file)
    filename = files.save(upload_file)
    # 如果是多文件上传
    # for filename in request.files.getlist('photo'):
        # photos.save(filename)
    logger.info(filename)
    logger.info("path: %s", files.path(filename))
    logger.info("url: %s", files.url(filename))
    return webJson(RetCode.SUCCESS)


@user.route('/download', methods=["GET"])
def test_download():
    """这里只能下载英文格式的文件，而且效率低下，需要用X-Sendfile的方式让nginx代理"""
    filename = requestGetParam(request, 'file')
    filename_path = files.path(filename)
    logger.info('________: %s', filename_path)
    return send_file(filename_path, as_attachment=True)


@token_auth.error_handler
def tokenUnauthorized():
    return webJson(RetCode.NEED_LOGIN)


@basic_auth.error_handler
def basicUnauthorized():
    return webJson(RetCode.NEED_LOGIN)


@basic_auth.verify_password
def verifyPassword(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@token_auth.verify_token
def verify_token(token):
    """在所有有@auth.login_required的路由中，认证成功的g.user都会被自动赋值，认证失败的也不会进入路由中"""
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True
