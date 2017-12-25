# coding: utf-8

from flask import Blueprint, session, request
from flask_login import login_user, logout_user, login_required

from .. import db
from ..models import User
from utils import requestGetParam, RetCode, webJson


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
def login():
    email = requestGetParam(request, 'email')
    passwd = requestGetParam(request, 'password')
    remember_me = requestGetParam(request, 'remember_me')
    user = User.query.filter_by(email=email).first()

    if user is not None and user.verify_password(passwd):
        login_user(user, remember_me)
        return webJson(RetCode.SUCCESS)
    return webJson(RetCode.LOGIN_ERROR)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    data = '已成功退出登陆'
    return webJson(RetCode.SUCCESS, data=data)


@user.route('/test_login')
def tst():
    if 'user_id' in session:
        return '<h1>you are still in</h1>'
    else:
        return '<h1>you have logouted</h1>'
