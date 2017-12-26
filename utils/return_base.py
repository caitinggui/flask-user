# coding: utf-8

from flask import jsonify


class RetCode(object):

    SUCCESS = (0, "访问成功")
    LOGIN_ERROR = (2001, "用户名或密码错误")
    EMAIL_DUPLICATION = (2002, "邮箱已注册")
    PARAMS_ERROR = ('2003', "参数有误")
    FILE_SUFFIX_ERROR = ('2004', "文件后缀有误")
    AVATAR_TOO_BIG = ('2005', "头像文件过大")
    FILE_NOT_EXITSTS = ('2006', "文件不存在")
    NEED_LOGIN = (401, "您需要登陆")
    PERMISSION_REQUIED = (403, "权限不足")
    PAGE_NOT_FOUND = (404, "此页面不存在")
    SERVER_ERROR = (500, "服务器异常，紧急修复中...")


def webJson(status, data=''):
    result = {
        "code": status[0],
        "msg": status[1],
        "data": data
    }
    return jsonify(result)
