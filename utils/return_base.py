# coding: utf-8

from flask import jsonify

class RetCode(object):

    SUCCESS = (0, "访问成功")
    LOGIN_ERROR = (2001, "用户名或密码错误")
    EMAIL_DUPLICATION = (2002, "邮箱已注册")
    NEED_LOGIN = (401, "您需要登陆")
    PAGE_NOT_FOUND = (404, "次页面不存在")


def webJson(status, data=''):
    result = {
        "code": status[0],
        "msg": status[1],
        "data": data
    }
    return jsonify(result)
