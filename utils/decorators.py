# coding: utf-8

from functools import wraps

from flask import g

from . import webJson, RetCode


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def mywrap(*args, **kwargs):
            if not g.user.can(permission):
                return webJson(RetCode.PERMISSION_REQUIED)
            return f(*args, **kwargs)
        return mywrap
    return decorator
