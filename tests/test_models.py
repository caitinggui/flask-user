# coding: utf-8

import unittest
import logging
import json
from base64 import b64encode

from utils import AppConfig
# 修改了全局的, 要在使用AppConfig之前, 验证已生效
AppConfig.SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
from apps import createApp, db
from apps.models import User


logger = logging.getLogger("test")


class CaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = createApp()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @property
    def auth_header(self, username="test", password="test"):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    @property
    def admin_header(self):
        pass

    def getCode(self, response):
        return json.loads(response.data)['code']

    def getData(self, response):
        return json.loads(response.data)['data']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @unittest.skip('for example')
    def testStatus(self):
        response = self.client.get('/')
        self.assertEqual(self.getCode(response), 0)

    def testLogin(self):
        res = self.client.get('/user/login', headers=self.auth_header)
        self.assertEqual(self.getCode(res), 401)
