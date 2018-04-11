import unittest
import os
import json
from app import create_app, db
from app.models import Review
from app.models import Business 
 
class TestReviewClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        #Testing data
        self.user_data = {'username':'kezzy', 'email':'user@email.com', 'password':'user_password', 'confirm_password':'user_password'}
        self.user_login_data = { 'username':'kezzy','password':'user_password'}
        
        self.reviews = {'title':'my review', 'content':'my reviews content'}
        self.reviews1 = {'title':'', 'content':'my reviews content'}
        self.reviews2 = {'title':'my review', 'content':''}
        self.business = {'business_name':'my business', 'about':'about', 'location':'location', 'category':'category'}
   
        with self.app.app_context():
        #Create all testing tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self):
        """Register a test user"""
        return self.client.post('/api/v1/auth/register', data=self.user_data)

    def login_user(self):
        """Test user to login"""
        return self.client.post('/api/v1/auth/login', data=self.user_login_data)


    def test_no_business_available(self):
        """Test if review is created"""
        #Ensure user is registered and logged in
        self.register_user()
        result=self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response=self.client.post('/api/v1/businesses/1/review', headers=dict(Authorization="Bearer " + access_token), data = self.reviews)
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("No business available", response_msg["message"])

    def test_no_business_with_given_id(self):
        """Test if review is not created if given id does not exist"""
        #Ensure user is registered and logged in
        self.register_user()
        result=self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token),data=self.business)
        response=self.client.post('/api/v1/businesses/18/review', headers=dict(Authorization="Bearer " + access_token), data = self.reviews)
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("No business with the given id", response_msg["message"])
        
        
    def test_incomplete_info(self):
        """Test if review is not created with incomplete information"""
        #Ensure user is registered and logged in
        self.register_user()
        result=self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token),data=self.business)
        response = self.client.post('/api/v1/businesses/1/review', headers=dict(Authorization="Bearer " + access_token),data=self.reviews1)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Incomplete Information", response_msg["message"])


    def test_review_created(self):
        """Test if review is created"""
        #Ensure user is registered and logged in
        self.register_user()
        result=self.login_user()


        access_token = json.loads(result.data.decode())['access_token']

        #create business
        response1 = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token),data=self.business)
        self.assertEqual(response1.status_code, 201)
        #create review
        response=self.client.post('/api/v1/businesses/1/review', headers=dict(Authorization="Bearer " + access_token), data = self.reviews)
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Review added successfully", response_msg["message"])

    # def view_reviews(self):
    #     self.client.post('/api/v1/businesses', data=self.business)
    #     self.client.post('/api/v1/businesses/1/review', data = self.reviews)
    #     response=self.client.get('/api/v1/businesses/1/review')
    #     self.assertEqual(response.status_code, 302)
 
