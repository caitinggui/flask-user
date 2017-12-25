# coding: utf-8
"""
permission_required装饰器要在login_required下面
login时自己处理表单，不要用basic_auth，这里仅是演示
后面的登陆验证只允许用token_auth!!!
"""

from flask import Blueprint, request, g

from .. import db, basic_auth, token_auth, multi_auth
from ..models import User, Permission
from utils import requestGetParam, RetCode, webJson, permission_required


user = Blueprint('user', __name__)


@user.route("/regist", methods=["GET", "POST"])
def regist():
    email = requestGetParam(request, 'email')
    passwd = requestGetParam(request, 'password')
    user = User()
    user.email = email
    user.password = passwd
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        return webJson(RetCode.EMAIL_DUPLICATION)
    return webJson(RetCode.SUCCESS)


@user.route('/login', methods=['GET', 'POST'])
@basic_auth.login_required
def login():
    """获取token只允许用账号和密码，禁止用token更新token.
    这里最好不用login_required，而是自己处理一个表单，
    然后把token返回去，后续再使用token_auth"""
    token = g.user.generate_auth_token()
    return webJson(RetCode.SUCCESS, data=token)


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
