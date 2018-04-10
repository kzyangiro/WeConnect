import unittest
import json
from app import create_app, db


class TestUserClass(unittest.TestCase):
    """Class for testing user model"""
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        """data for testing our app"""
        self.user_data = { 'username':'kezzy', 'email':'user@email.com', 'password':'user_password', 'confirm_password':'user_password'}
        self.user_data_duplicate_email = { 'username':'Ann', 'email':'user@email.com', 'password':'ann_password', 'confirm_password':'ann_password'}
        self.user_data_unmatching_pwd = { 'username':'kezzy', 'email':'user@email.com', 'password':'user_password', 'confirm_password':'user_password1'}
        self.user_data_invalid_email = { 'username':'kezzy', 'email':'user', 'password':'user_password', 'confirm_password':'user_password'}
        self.user_login_data = { 'username':'kezzy','password':'user_password'}
        self.user_login_unregistered = { 'username':'Newkezzy','password':'Newuser_password'}

        self.reset_pwd_data = {'username':'kezzy','password':'user_password','new_password':'pwd','confirm_password':'pwd'}
        
        with self.app.app_context():
            """ create tables for out testing data"""
            db.session.close()
            db.drop_all()
            db.create_all()

    #To reset password and to logout, we need to have an registered user login
    def register_user(self):
        """Register a test user"""
        return self.client.post('/api/v1/auth/register', data=self.user_data)

    def login_user(self):
        """Test user to login"""
        return self.client.post('/api/v1/auth/login', data=self.user_login_data)

    def test_registration(self):
        """ Test if user is registered successfully"""
        res = self.client.post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'User Registered successfully')

    def test_unmatching_passwords(self):
        """ Test if password does not match with 'confirm_password' """
        res = self.client.post('/api/v1/auth/register', data=self.user_data_unmatching_pwd)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Unmatched passwords')

    def test_invalid_email(self):
        """ Test if email provided is not in a valid email format"""
        res = self.client.post('/api/v1/auth/register', data=self.user_data_invalid_email)
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Invalid email address')


    def test_already_registered_username(self):
        """ Test if username provided is already registered """
        res = self.client.post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)

        res1 = self.client.post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res1.status_code, 409)


        result = json.loads(res1.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'The username is already registered, kindly chose a different one')

    def test_already_registered_email(self):
        """ Test if email provided is already registered """
        res = self.client.post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)

        res1 = self.client.post('/api/v1/auth/register', data=self.user_data_duplicate_email)
        self.assertEqual(res1.status_code, 409)


        result = json.loads(res1.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'The email is already registered, kindly chose a different one')


    def test_user_login(self):
        """ Test if user can successfully login given correct username and password """
        res = self.client.post('/api/v1/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)

        res_login = self.client.post('/api/v1/auth/login', data=self.user_login_data)
        self.assertEqual(res_login.status_code, 200)

        result = json.loads(res_login.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'User Logged in successfully')

        self.assertTrue(result['access_token'])
        

    def test_login_unregistered_user(self):
        """ Test if unregistered user or wrong credentials is unable to login """
        res_login = self.client.post('/api/v1/auth/login', data=self.user_login_unregistered)
        self.assertEqual(res_login.status_code, 404)

        result = json.loads(res_login.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Wrong username or password entered')

    def test_user_logs_in_with_null_username_and_or_password(self):
        """Test if User can't log in with empty fields"""
        self.client.post('/api/v1/auth/register', data=self.user_data)
        res=self.client.post('/api/v1/auth/login', data={"username":"", "password":"password"})
        self.assertEqual(res.status_code, 400)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['message'], 'Input empty fields')

    def test_reset_password(self):

        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        """Tests if an authenticated user can reset password"""       
        res = self.client.put('/api/v1/auth/reset_password', headers=dict(Authorization="Bearer " + access_token), data=self.reset_pwd_data)

        self.assertEqual(res.status_code, 200)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['message'], 'Password reset successfully')