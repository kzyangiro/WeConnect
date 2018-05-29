import unittest
import json
from app import create_app, db
from flask_bcrypt import Bcrypt


class TestUser(unittest.TestCase):
    """Class for testing user model"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        self.register_data = { 'username':'kezzy', 'email':'kzynjokerio@gmail.com', 'password':'@kzy12', 'confirm_password':'@kzy12'}

        """bind app to the current context"""
        with self.app.app_context():
            db.create_all()

        """ Initial input """
        self.client.post(TestUser.register, data=self.register_data)
        self.token = json.loads(self.client.post(TestUser.login, data={ 'username':'kezzy','password':'@kzy12'}).data.decode())['access_token']

    """ Endpoints to test """
    register = '/api/v1/auth/register'
    login = '/api/v1/auth/login'
    logout = '/api/v1/auth/logout'
    change_pwd = '/api/v1/auth/update_password'

    def test_new_user_registration(self):
        """ Test if api can register a new user"""

        res = self.client.post(TestUser.register, data={ 'username':'Milly', 'email':'milly@gmail.com', 'password':'@mkzy12', 'confirm_password':'@mkzy12'})
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'User Registered successfully')

    def test_new_user_registration_with_unmatched_passwords(self):
        """ Test if api can't register user with non matching passwords"""

        res = self.client.post(TestUser.register, data={ 'username':'Ann', 'email':'ann@email.com', 'password':'@kzy12', 'confirm_password':'@kzy12rrr'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Unmatched passwords')

    def test_new_user_registration_with_invalid_passwords(self):
        """ Test if api can't register user with a weak password. Password should be a length of 6, have at leas one letter, one word and one special character"""

        res = self.client.post(TestUser.register, data={ 'username':'Ann', 'email':'ann@email.com', 'password':'ann', 'confirm_password':'ann'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Kindly set a strong password. Ensure to use aminimum of 6 characters that contains at least 1 letter, one number and one special character')

    def test_new_user_registration_with_username_of_less_that_3_character(self):
        """ Test if api can't register user with less than 3 characters of the username"""

        res = self.client.post(TestUser.register, data={ 'username':'A', 'email':'anny@email.com', 'password':'@kzy12', 'confirm_password':'@kzy12'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Kindly set a username of more than 3 letters')


    def test_new_user_registration_with_invalid_input(self):
        """ Test if api can't register user with an invalid input i.e using integers as input"""

        res = self.client.post(TestUser.register, data={ 'username':"88888", 'email':'annette@gmail.com', 'password':'@kzy12', 'confirm_password':'@kzy12'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], "kindly use only letters for a username")

    def test_new_user_registration_with_invalid_email(self):
        """ Test if api can't register user with an invalid email format"""

        res = self.client.post(TestUser.register, data={ 'username':'Ann', 'email':'ann', 'password':'@kzy12', 'confirm_password':'@kzy12'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Invalid email address')


    def test_new_user_registration_with_already_registered_username(self):
        """ Test if api can't register user with an already registered username """
        res1 = self.client.post(TestUser.register, data=self.register_data)
        self.assertEqual(res1.status_code, 409)

        result = json.loads(res1.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'The username is already registered, kindly chose a different one')

    def test_new_user_registration_with_already_registered_email(self):
        """ Test if api can't register user with an already registered email """
        res = self.client.post(TestUser.register, data={ 'username':'Ann', 'email':'kzynjokerio@gmail.com', 'password':'@kzy12', 'confirm_password':'@kzy12'})
        
        self.assertEqual(res.status_code, 409)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'The email is already registered, kindly chose a different one')


    def test_login_registered_user(self):
        """ Test if api can login a registered user when correct username and password is filled in """
        res_login = self.client.post(TestUser.login, data={ 'username':'kezzy','password':'@kzy12'})
        self.assertEqual(res_login.status_code, 200)

        result = json.loads(res_login.data.decode('UTF-8'))
        self.assertEqual(result['Message'], 'Successfully Logged in')

    def test_login_unregistered_user(self):
        """ Test if api can't login an unregistered user"""
        res_login = self.client.post(TestUser.login, data={ 'username':'Annie','password':'@kzy12'})
        self.assertEqual(res_login.status_code, 200)

        result = json.loads(res_login.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Invalid username')


    def test_login_with_wrong_password(self):
        """ Test if api can't login when correct valid username is provided but password is wrong """
        res_login = self.client.post(TestUser.login, data={ 'username':'kezzy','password':'yyyy@kzy12'})
        self.assertEqual(res_login.status_code, 401)

        result = json.loads(res_login.data.decode('UTF-8'))
        self.assertEqual(result['message'], 'Wrong password entered')

    def test_login_with_empty_fields(self):
        """Test if api can't login user with empty fields"""
        res=self.client.post(TestUser.login, data={"username":"", "password":"@kzy12"})
        self.assertEqual(res.status_code, 400)

        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['message'], 'Invalid input, fill in all required inputs, and kindly use strings')

    def test_logout(self):
        """Test if api can log out a logged in user"""

        res = self.client.post(TestUser.logout, headers=dict(Authorization="Bearer " + self.token))

        self.assertEqual(res.status_code, 200)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['message'], 'Successfully Logged Out')

    def test_logout_with_invalid_access_token(self):
        """Test if api cannot logout if access token is invalid"""

        res = self.client.post(TestUser.logout, headers=dict(Authorization="Bearer " + 'wrong_access_token'))

        self.assertEqual(res.status_code, 401)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['message'], 'Invalid token, Login to obtain a new token')


    def test_change_password(self):
        """Test if api can change password for a logged in user"""

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + self.token), data={'email':'kzynjokerio@gmail.com','current_password':'@kzy12', 'new_password':'@kzy12kzy','confirm_password':'@kzy12kzy'})

        self.assertEqual(res.status_code, 200)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['message'], 'Password updated successfully')


    def test_change_password_with_invalid_token(self):
        """Test if api cannot change password if the token provided is expired or invalid"""
        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + "12345"), data={'email':'kzynjokerio@gmail.com','current_password':'@kzy12', 'new_password':'@kzy12kzy','confirm_password':'@kzy12kzy'})

        self.assertEqual(res.status_code, 401)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['message'], 'Invalid token, Login to obtain a new token')

    def test_change_password_with_incomplete_information(self):
        """Test if api cannot change password if not all input fields are filled in"""

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + self.token), data={'current_password':'user_password', 'new_password':'@kzy12','confirm_password':'@kzy12'})

        self.assertEqual(res.status_code, 400)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['message'], 'Invalid input, kindly fill in all required input')

    def test_change_password_with_invalid_email(self):
        """Test if api cannot change password if email filled in is not registered"""

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + self.token), data={'email':'njokerio@gmail.com','current_password':'@kzy12', 'new_password':'@kzy12kzy','confirm_password':'@kzy12kzy'})

        self.assertEqual(res.status_code, 200)
        res_msg = json.loads(res.data.decode("UTF-8"))

        self.assertEqual(res_msg['error'], 'Invalid Email')

    def test_change_password_with_wrong_password(self):
        """Test if api cannot change password if current password indicated is not correct"""

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + self.token), data={'email':'kzynjokerio@gmail.com','current_password':'@kzy12rrr', 'new_password':'@kzy12kzy','confirm_password':'@kzy12kzy'})

        self.assertEqual(res.status_code, 400)
        res_msg = json.loads(res.data.decode("UTF-8"))

        self.assertEqual(res_msg['error'], 'Wrong password')

    def test_change_password_with_non_matching_new_and_confirm_passwords(self):
        """Test if api cannot change password if new and confirm passwords are not matching"""

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + self.token), data={'email':'kzynjokerio@gmail.com','current_password':'@kzy12', 'new_password':'@kzy121','confirm_password':'@kzy12'})

        self.assertEqual(res.status_code, 400)
        res_msg = json.loads(res.data.decode("UTF-8"))

        self.assertEqual(res_msg['message'], 'Passwords not matching')


    def tearDown(self):
        """clear all test variables."""
        with self.app.app_context():
            "Delete all tables"
            db.session.remove()
            db.drop_all()