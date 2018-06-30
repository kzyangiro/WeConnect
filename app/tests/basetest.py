import unittest
from unittest import TestCase
import json
from app import create_app, db

class BaseTestCase(TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        self.register_data = { 'username':'kezzy', 'email':'kzynjokerio@gmail.com', 'password':'@kzy12', 'confirm_password':'@kzy12'}

        """bind app to the current context"""
        with self.app.app_context():
            db.create_all()

        """ Initial input """
        self.client.post(BaseTestCase.register, data=self.register_data)
        self.token = json.loads(self.client.post(BaseTestCase.login, data={ 'username':'kezzy','password':'@kzy12'}).data.decode())['access_token']

    """ Endpoints to test """
    register = '/api/v1/auth/register'
    login = '/api/v1/auth/login'
    logout = '/api/v1/auth/logout'
    change_pwd = '/api/v1/auth/update_password'
    reset_pwd = '/api/v1/auth/reset_password'