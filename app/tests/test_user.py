import unittest
import json
from app import create_app, db


class TestUser(unittest.TestCase):
    """Class for testing user model"""
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        """bind app to the current context"""
        with self.app.app_context():
            """create test tables"""
            db.create_all()

    """ Endpoints to test """

    register = '/api/v1/auth/register'
    login = '/api/v1/auth/login'
    change_pwd = '/api/v1/auth/update_password'
    reset_pwd = '/api/v1/auth/reset_password'

    #To reset password and to logout, we need to have an registered user login
    def register_user(self):
        """Register a test user"""

        return self.client.post(TestUser.register, data={ 'username':'kezzy', 'email':'user@email.com', 'password':'user_password', 'confirm_password':'user_password'})

    def login_user(self):
        """Login registered test user"""

        return self.client.post(TestUser.login, data={ 'username':'kezzy','password':'user_password'})

    def test_new_user_registration(self):
        """ Test if api can register a new user"""

        res = self.register_user()
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'User Registered successfully')

    def test_new_user_registration_with_unmatched_passwords(self):
        """ Test if api can't register user with non matching passwords"""

        res = self.client.post(TestUser.register, data={ 'username':'Ann', 'email':'ann@email.com', 'password':'ann', 'confirm_password':'ann1'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Unmatched passwords')

    def test_new_user_registration_with_invalid_email(self):
        """ Test if api can't register user with an invalid email format"""

        res = self.client.post(TestUser.register, data={ 'username':'Ann', 'email':'ann', 'password':'ann', 'confirm_password':'ann'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Invalid email address')


    def test_new_user_registration_with_already_registered_username(self):
        """ Test if api can't register user with an already registered username """
        self.register_user()
        res1 = self.register_user()
        self.assertEqual(res1.status_code, 409)

        result = json.loads(res1.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'The username is already registered, kindly chose a different one')

    def test_new_user_registration_with_already_registered_email(self):
        """ Test if api can't register user with an already registered email """
        self.register_user()
        res = self.client.post(TestUser.register, data={ 'username':'Ann', 'email':'user@email.com', 'password':'ann', 'confirm_password':'ann'})
        
        self.assertEqual(res.status_code, 409)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'The email is already registered, kindly chose a different one')


    def test_login_registered_user(self):
        """ Test if api can login a registered user when correct username and password is filled in """
        self.register_user()
        res_login = self.login_user()
        self.assertEqual(res_login.status_code, 200)

        result = json.loads(res_login.data.decode('UTF-8'))
        self.assertEqual(result['Message'], 'Successfully Logged in')

        self.assertTrue(result['access_token'])
        

    def test_login_unregistered_user(self):
        """ Test if api can't login an unregistered user"""
        res_login = self.client.post(TestUser.login, data={ 'username':'kezzy','password':'user_password'})
        self.assertEqual(res_login.status_code, 404)

        result = json.loads(res_login.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Invalid username')


    def test_login_with_wrong_password(self):
        """ Test if unregistered user or wrong credentials is unable to login """
        self.register_user()
        res_login = self.client.post(TestUser.login, data={ 'username':'kezzy','password':'wrong_pwd'})
        self.assertEqual(res_login.status_code, 401)

        result = json.loads(res_login.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Wrong password entered')

    def test_login_with_empty_fields(self):
        """Test if api can't login user with empty fields"""
        self.register_user()
        res=self.client.post(TestUser.login, data={"username":"", "password":"password"})
        self.assertEqual(res.status_code, 400)

        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['message'], 'Invalid input, kindly fill in all required input')

    def test_change_password(self):
        """Test if api can change password for a logged in user"""

        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + access_token), data={'email':'user@email.com','current_password':'user_password', 'new_password':'pwd','confirm_password':'pwd'})

        self.assertEqual(res.status_code, 200)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['message'], 'Password updated successfully')

    def test_reset_password(self):
        """Test if api can reset password for a registered user when correct email and username are filled in"""

        self.register_user()
        """Tests if an authenticated user can reset password"""       
        res = self.client.put(TestUser.reset_pwd, data={'username':'kezzy', 'email':'user@email.com','new_password':'pwd','confirm_password':'pwd'})

        self.assertEqual(res.status_code, 200)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['message'], 'Password reset successfully')


    def tearDown(self):
        """clear all test variables."""
        with self.app.app_context():
            "Delete all tables"
            db.session.remove()
            db.drop_all()