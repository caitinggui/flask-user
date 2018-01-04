#! env/bin/python
# coding: utf-8

import os
import logging
import logging.config

import click  # 要import，不然app.cli.command不生效
from werkzeug.exceptions import HTTPException

from apps import createApp
from utils import RetCode, webJson, ParamsError
from configs.log_config import log_config


PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))


logging.config.dictConfig(log_config)
logger = logging.getLogger("apps")


app = createApp()


@app.errorhandler(401)
def handle401(error):
    return webJson(RetCode.NEED_LOGIN)


@app.errorhandler(404)
def handle404(error):
    return webJson(RetCode.PAGE_NOT_FOUND)


@app.errorhandler(ParamsError)
def handleParamsError(error):
    return webJson(RetCode.PARAMS_ERROR, data=error.data)


@app.errorhandler(Exception)
def internal_server_error(e):
    logger.exception("SERVER ERROR 500: %s", e)
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return webJson(RetCode.SERVER_ERROR, data=code)


@app.cli.command(short_help='Runs a ipython shell in the app context.')
def ishell():
    from IPython import embed
    from apps import db
    from apps.models import User, Role, Permission
    embed()


@app.cli.command(short_help='Runs testcase')
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.route('/')
def index():
    return "hello"


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
