import unittest, os, re, json
from app import create_app
from app.models import User
 
class TestUserClass(unittest.TestCase):
    """Class for testing user model"""
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        """data for testing"""
        self.user1 = {'username':'Ann', 'email':'ann@gmail.com', 'password':'mypwd', 'confirm_password':'mypwd'}
        self.user = {'username':'Kezzy', 'email':'kezzy@gmail.com', 'password':'mypwd', 'confirm_password':'mypwd'}
        self.login = {'username':'Kezzy', 'password':'mypwd'}

 
    def test_register_user(self):
        """test if user is created"""   
        response = self.client.post('/api/v1/auth/register', data=self.user1)
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual('User Created successfully', response_msg["message"])

    def test_user_login(self):
        """user logs in"""
        self.client.post('/api/v1/auth/register', data=self.user)
        result=self.client.post('/api/v1/auth/login', data=self.login)
        self.assertEqual(result.status_code, 200)


    def test_user_logout(self):
        """user logs out"""
        self.client.post('/api/v1/auth/register', data=self.user)
        result=self.client.post('/api/v1/auth/login', data=self.login)
        
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post('/api/v1/auth/logout', headers=dict(Authorization="Bearer " + access_token))
        
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Successfully Logged Out", response_msg["message"])





    def tearDown(self):
        """Clear user list when testing is completed"""
        User.user=[]
        
