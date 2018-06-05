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
    reset_pwd = '/api/v1/auth/reset_password'

    def test_new_user_registration(self):
        """ Test if api can register a new user"""

        res = self.client.post(TestUser.register, data={ 'username':'Milly', 'email':'milly@gmail.com', 'password':'@mkzy12', 'confirm_password':'@mkzy12'})
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['Success'], 'User Registered successfully')

    def test_new_user_registration_with_incomplete_details(self):
        """ Test if api can't register user with some details missing """

        res = self.client.post(TestUser.register, data={'email':'ann@email.com', 'password':'@kzy12', 'confirm_password':'@kzy12'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['Error'], 'Invalid input, fill in all required input and kindly use valid strings')

    def test_new_user_registration_with_tabs_as_input(self):
        """ Test if api can register a new user"""

        res = self.client.post(TestUser.register, data={ 'username':'   ', 'email':'milly@gmail.com', 'password':'@mkzy12', 'confirm_password':'@mkzy12'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['Error'], 'Input empty fields')

    def test_new_user_registration_with_non_alphabetic_username(self):
        """ Test if api can't register user with an invalid input i.e using integers as input"""

        res = self.client.post(TestUser.register, data={ 'username':"88888", 'email':'annette@gmail.com', 'password':'@kzy12', 'confirm_password':'@kzy12'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['Error'], "kindly use only letters for a username")

    def test_new_user_registration_with_username_of_less_that_3_character(self):
        """ Test if api can't register user with less than 3 characters of the username"""

        res = self.client.post(TestUser.register, data={ 'username':'A', 'email':'anny@email.com', 'password':'@kzy12', 'confirm_password':'@kzy12'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['Error'], 'Kindly set a username of more than 3 letters')

    def test_new_user_registration_with_invalid_password_strength(self):
        """ Test if api can't register user with a weak password. Password should be a length of 6, have at leas one letter, one word and one special character"""

        res = self.client.post(TestUser.register, data={ 'username':'Ann', 'email':'ann@email.com', 'password':'ann', 'confirm_password':'ann'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['Error'], 'Kindly set a strong password. Ensure to use aminimum of 6 characters that contains at least 1 letter, one number and one special character')

    def test_new_user_registration_with_unmatched_passwords(self):
        """ Test if api can't register user with non matching passwords"""

        res = self.client.post(TestUser.register, data={ 'username':'Ann', 'email':'ann@email.com', 'password':'@kzy12', 'confirm_password':'@kzy12rrr'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['Error'], 'Unmatched passwords')

    def test_new_user_registration_with_invalid_email_format(self):
        """ Test if api can't register user with an invalid email format"""

        res = self.client.post(TestUser.register, data={ 'username':'Ann', 'email':'ann', 'password':'@kzy12', 'confirm_password':'@kzy12'})
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['Error'], 'Invalid email address, kindly use the right email format i.e abc@def.com')


    def test_new_user_registration_with_already_registered_username(self):
        """ Test if api can't register user with an already registered username """
        res1 = self.client.post(TestUser.register, data=self.register_data)
        self.assertEqual(res1.status_code, 409)

        result = json.loads(res1.data.decode('UTF-8'))
        self.assertEqual(result['Error'], 'The username is already registered, kindly chose a different one')

    def test_new_user_registration_with_already_registered_email(self):
        """ Test if api can't register user with an already registered email """
        res = self.client.post(TestUser.register, data={ 'username':'Ann', 'email':'kzynjokerio@gmail.com', 'password':'@kzy12', 'confirm_password':'@kzy12'})
        
        self.assertEqual(res.status_code, 409)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['Error'], 'The email is already registered, kindly chose a different one')


    def test_login_registered_user(self):
        """ Test if api can login a registered user when correct username and password is filled in """
        res_login = self.client.post(TestUser.login, data={ 'username':'kezzy','password':'@kzy12'})
        self.assertEqual(res_login.status_code, 200)

        result = json.loads(res_login.data.decode('UTF-8'))
        self.assertEqual(result['Success'], 'Successfully Logged in')

    def test_login_with_empty_fields(self):
        """Test if api can't login user with empty fields"""
        res=self.client.post(TestUser.login, data={"username":"", "password":"@kzy12"})
        self.assertEqual(res.status_code, 400)

        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['Error'], 'Invalid input, fill in all required inputs, and kindly use strings')

    def test_login_with_tabs_as_input(self):
        """ Test if api can't login with tab spaces as input"""
        res_login = self.client.post(TestUser.login, data={ 'username':'kezzy','password':'   '})
        self.assertEqual(res_login.status_code, 400)

        result = json.loads(res_login.data.decode('UTF-8'))
        self.assertEqual(result['Error'], 'Fill in the empty fields')

    def test_login_unregistered_user(self):
        """ Test if api can't login an unregistered user"""
        res_login = self.client.post(TestUser.login, data={ 'username':'Annie','password':'@kzy12'})
        self.assertEqual(res_login.status_code, 200)

        result = json.loads(res_login.data.decode('UTF-8'))
        self.assertEqual(result['Error'], 'User not found, kindly use correct username')


    def test_login_with_wrong_password(self):
        """ Test if api can't login when correct valid username is provided but password is wrong """
        res_login = self.client.post(TestUser.login, data={ 'username':'kezzy','password':'yyyy@kzy12'})
        self.assertEqual(res_login.status_code, 401)

        result = json.loads(res_login.data.decode('UTF-8'))
        self.assertEqual(result['Error'], 'Wrong password entered')


    def test_logout(self):
        """Test if api can log out a logged in user"""

        res = self.client.post(TestUser.logout, headers=dict(Authorization="Bearer " + self.token))

        self.assertEqual(res.status_code, 200)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['Success'], 'Successfully Logged Out')

    def test_logout_with_invalid_access_token(self):
        """Test if api cannot logout if access token is invalid"""

        res = self.client.post(TestUser.logout, headers=dict(Authorization="Bearer " + 'wrong_access_token'))

        self.assertEqual(res.status_code, 401)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['Error'], 'Invalid token, Login to obtain a new token')

    def test_update_password(self):
        """Test if api can change password for a logged in user"""

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + self.token), data={'email':'kzynjokerio@gmail.com','current_password':'@kzy12', 'new_password':'@kzy12kzy','confirm_password':'@kzy12kzy'})

        self.assertEqual(res.status_code, 200)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['Success'], 'Password updated successfully')


    def test_change_password_with_invalid_token(self):
        """Test if api cannot change password if the token provided is expired or invalid"""
        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + "12345"), data={'email':'kzynjokerio@gmail.com','current_password':'@kzy12', 'new_password':'@kzy12kzy','confirm_password':'@kzy12kzy'})

        self.assertEqual(res.status_code, 401)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['Error'], 'Invalid token, Login to obtain a new token')

    def test_change_password_with_incomplete_information(self):
        """Test if api cannot change password if not all input fields are filled in"""

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + self.token), data={'current_password':'user_password', 'new_password':'@kzy12','confirm_password':'@kzy12'})

        self.assertEqual(res.status_code, 400)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['Error'], 'Invalid input, fill in all required input and kindly use valid strings')

    def test_update_password_with_tabs_as_input(self):
        """Test if api cannot change password with tab spaces as only input"""

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + self.token), data={'email':'    ','current_password':'@kzy12', 'new_password':'@kzy12kzy','confirm_password':'@kzy12kzy'})

        self.assertEqual(res.status_code, 400)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['Error'], 'Input Empty Fields')

    def test_change_password_with_invalid_email(self):
        """Test if api cannot change password if email filled in is not registered"""

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + self.token), data={'email':'njokerio@gmail.com','current_password':'@kzy12', 'new_password':'@kzy12kzy','confirm_password':'@kzy12kzy'})

        self.assertEqual(res.status_code, 200)
        res_msg = json.loads(res.data.decode("UTF-8"))

        self.assertEqual(res_msg['Error'], 'Unrecognised email, kindly ensure to use the email you registered with')

    def test_change_password_with_wrong_password(self):
        """Test if api cannot change password if current password indicated is not correct"""

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + self.token), data={'email':'kzynjokerio@gmail.com','current_password':'@kzy12rrr', 'new_password':'@kzy12kzy','confirm_password':'@kzy12kzy'})

        self.assertEqual(res.status_code, 400)
        res_msg = json.loads(res.data.decode("UTF-8"))

        self.assertEqual(res_msg['Error'], 'Wrong current password')

    def test_change_password_with_weak_passwords(self):
        """Test if api cannot change password if new password is weak and less than 6 characters"""

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + self.token), data={'email':'kzynjokerio@gmail.com','current_password':'@kzy12', 'new_password':'pwd','confirm_password':'pwd'})

        self.assertEqual(res.status_code, 400)
        res_msg = json.loads(res.data.decode("UTF-8"))

        self.assertEqual(res_msg['Error'], 'Kindly set a strong password. Ensure to use aminimum of 6 characters that contains at least 1 letter, one number and one special character')


    def test_change_password_with_non_matching_new_and_confirm_passwords(self):
        """Test if api cannot change password if new and confirm passwords are not matching"""

        res = self.client.put(TestUser.change_pwd, headers=dict(Authorization="Bearer " + self.token), data={'email':'kzynjokerio@gmail.com','current_password':'@kzy12', 'new_password':'@kzy121','confirm_password':'@kzy12'})

        self.assertEqual(res.status_code, 400)
        res_msg = json.loads(res.data.decode("UTF-8"))

        self.assertEqual(res_msg['Error'], 'New password not matching with confirm password')

    def test_reset_password_with_empty_input(self):
        """Test if api can't reset password with empty email input """

        res = self.client.post(TestUser.reset_pwd, data={'email':''})

        self.assertEqual(res.status_code, 400)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['Error'], 'Kindly fill in an email in a string format')

    def test_reset_password_with_invalid_email_format_input(self):
        """Test if api can't reset password for an invalid email format"""

        res = self.client.post(TestUser.reset_pwd, data={'email':'kzy.com'})

        self.assertEqual(res.status_code, 400)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual(res_msg['Error'], 'Fill in a valid email address and kindly use the right email format i.e abc@def.com')

    def tearDown(self):
        """clear all test variables."""
        with self.app.app_context():
            "Delete all tables"
            db.session.remove()
            db.drop_all()