# coding: utf-8
'''
存储一些配置和常量
'''

import os

from configs.config import dbconfigs


# 项目的主目录，既configs的父级目录
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mysql = dbconfigs["mysql"]


class Constant(object):
    avatar_basedir = 'static/avatars'
    avatar_folder_size = 1000
    avatar_max_size = 2 * 1024 * 1024  # 头像大小最大为2MB


class AppConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    # SERVER_NAME = 'http://flask-user.com'

    # 使用sqlite是无法使用pool_size等参数
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.db')
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(mysql["USER"], mysql["PASSWORD"], mysql["HOST"], mysql["PORT"], mysql["DB"])
    # SQLALCHEMY_POOL_SIZE = mysql['POOLSIZE']  # 连接池大小
    # SQLALCHEMY_MAX_OVERFLOW = 20  # 在超出连接池后可以新增的线程数，这些线程用后即销毁
    # SQLALCHEMY_POOL_RECYCLE = 60 * 60 * 2  # 不同的数据库不同的数值，当为MySQL时默认为2h
    # 追踪对象的修改并且发送信号，比较耗内存,在需要监听signal时需要用到
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # 是否显示sqlalchemy的log，适用于debug

    # uploads的配置
    UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'media')
    # 对于没有指定路径的set，默认会在UPLOADS_DEFAULT_DEST后面加上set的名字
    # 为flask-upload 的set为photos设置的地址，如果set名字为file, 那么就是UPLOADED_FILE_DEST
    UPLOADED_PHOTOS_DEST = basedir  # 在使用的时候加上Constant.avatar_basedir
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 1MB, 全局的，用户头像上传时还要单独判断一下
