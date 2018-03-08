import unittest
import os
import json
from app import create_app
from app.models import User
 
class TestUserClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.user = {'username':'Kezzy', 'email':'kezzy@gmail.com', 'password':'mypwd', 'confirm_password':'mypwd'}
        self.login = {'username':'Kezzy', 'password':'password'}
        self.old_user = {'username':'Kezzy', 'email':'kezzy@gmail.com', 'password':'mypwd', 'confirm_password':'mypwd'}
 
    def test_register_user(self):   
        """api tests if a user is created
        Returns Created if created"""     
        response = self.client.post('/api/v1/auth/register', data=self.user)
        if self.user["username"] and self.user["email"] and self.user["password"] and self.user["confirm_password"]:


            if self.user["email"]:
                self.assertEqual(response.status_code, 403)
                response_msg = json.loads(response.data.decode("UTF-8"))
                self.assertIn("Invalid email address", response_msg["message"])

            elif self.old_user["email"] == self.user["email"]:
                self.assertEqual(response.status_code,403)            
                response_msg = json.loads(response.data.decode("UTF-8"))
                self.assertIn("The email address already exist use a different one", response_msg["message"])

            elif self.old_user["username"] == self.user["username"]:
                self.assertEqual(response.status_code,403)
                response_msg = json.loads(response.data.decode("UTF-8"))
                self.assertIn("The username already exist use a different one", response_msg["message"])
            elif self.user["password"] != self.user["confirm_password"]:
                self.assertEqual(response.status_code, 403)
                response_msg = json.loads(response.data.decode("UTF-8"))
                self.assertIn("Unmatched passwords", response_msg["message"])

            else:
                self.assertEqual(response.status_code, 201)
                response_msg = json.loads(response.data.decode("UTF-8"))
                self.assertIn("User Created successfully", response_msg["message"])

        else:
            self.assertEqual(response.status_code, 403)
            response_msg = json.loads(response.data.decode("UTF-8"))
            self.assertIn("Input empty fields", response_msg["message"])
                
        
    def user_login(self):
        """user creates account"""
        result=self.client().post('/api/v1/auth/register', data=self.user)

        """user logs in"""
        res=self.client.post('/api/v1/auth/login', data=self.login)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertIn("Logged in successful", res_msg["message"])

    def test_user_logs_in_with_wrong_username_and_or_password(self):
        result=self.client.post('/api/v1/auth/register', data=self.user)
        """User logs in with wrong username"""
        res=self.client.post('/api/v1/auth/login', data={"username":"kerry", "password":"password"})
        self.assertEqual(res.status_code, 404)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertIn("Wrong username or password entered", res_msg["message"])


    def test_user_logs_in_with_null_username_and_or_password(self):
        result=self.client.post('/api/v1/auth/register', data=self.user)
        """User logs in with wrong username"""
        res=self.client.post('/api/v1/auth/login', data={"username":"", "password":"password"})
        self.assertEqual(res.status_code, 403)
        res_msg = json.loads(res.data.decode("UTF-8"))
        self.assertIn("Empty username or password field", res_msg["message"])

    #Clear my list

    def tearDown(self):
        User.user=[]
        
