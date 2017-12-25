# coding: utf-8

import os

basedir = os.path.dirname(os.path.abspath(__file__))


class AppConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    # 追踪对象的修改并且发送信号，比较耗内存,在需要监听signal时需要用到
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@127.0.0.1/test'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_ECHO = False  # 是否显示sqlalchemy的log，适用于debug
    SQLALCHEMY_POOL_SIZE = 20  # 连接池大小
    SQLALCHEMY_MAX_OVERFLOW = 20  # 在超出连接池后可以新增的线程数，这些线程用后即销毁
    SQLALCHEMY_POOL_RECYCLE = 60 * 60 * 2  # 不同的数据库不同的数值，当为MySQL时默认为2h
