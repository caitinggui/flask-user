# coding: utf-8


def requestGetParam(request, key, default=None):
    param = request.args.get(key, default)
    return param
