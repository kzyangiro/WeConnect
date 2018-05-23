import unittest
import os
import json
from app import create_app, db
from app.models import Review
from app.models import Business 
 
class TestReview(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

        """ Initial Input"""
        self.client.post(TestReview.register, data={'username':'kezzy', 'email':'user@email.com', 'password':'user_password', 'confirm_password':'user_password'})
        result = self.client.post(TestReview.login, data={ 'username':'kezzy','password':'user_password'})
        self.token = json.loads(result.data.decode())['access_token']
        self.client.post(TestReview.business, headers=dict(Authorization="Bearer " + self.token), data={'business_name':'my business', 'about':'about', 'location':'location', 'category':'category'})

        self.client.post(TestReview.business+'/1/review', headers=dict(Authorization="Bearer " + self.token), data = {'content':'my reviews content'})

    """ Endpoints to test """

    register = '/api/v1/auth/register'
    login = '/api/v1/auth/login'
    business = '/api/v1/businesses'


    def test_creating_a_review_when_the_business_indicated_does_not_exist(self):
        """Test if review is not created if business indicated is not available"""
        response=self.client.post(TestReview.business+'/2/review', headers=dict(Authorization="Bearer " + self.token), data = {'content':'my reviews content'})
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("No business with the given id", response_msg["message"])
    
    def test_creating_a_review_using_an_invalid_token(self):
        """Test if review is not created if token used is invalid"""
        response=self.client.post(TestReview.business+'/2/review', headers=dict(Authorization="Bearer " + '12345'), data = {'content':'my reviews content'})
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Invalid token, Login to obtain a new token", response_msg["message"])  

    def test_creating_a_review_using_numbers_only(self):
        """Test if review is not created if only digits are filled in"""
        response=self.client.post(TestReview.business+'/2/review', headers=dict(Authorization="Bearer " + self.token), data = {'content':'12345'})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Invalid input, kindly use alphabets also for input", response_msg["message"]) 

    def test_create_review_with_incomplete_information(self):
        """Test if review is not created with incomplete information"""

        response=self.client.post(TestReview.business+'/1/review', headers=dict(Authorization="Bearer " + self.token), data = {'content':''})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Invalid input, kindly fill in all required input", response_msg["message"])


    def test_create_a_review(self):
        """Test if api can create a review"""
        response=self.client.post(TestReview.business+'/1/review', headers=dict(Authorization="Bearer " + self.token), data = {'content':'Awesome'})
        
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Review added successfully", response_msg["Message"])


    def test_view_reviews(self):
        """Test if api can retrieve reviews"""
        
        response=self.client.get(TestReview.business+'/1/review')
        self.assertEqual(response.status_code, 200)

    def test_view_reviews_but_no_reviews_available_for_that_business(self):
        """Test if api cannot  retrieve reviews when none exists"""

        self.client.post(TestReview.business, headers=dict(Authorization="Bearer " + self.token), data={'business_name':'Andela', 'about':'about', 'location':'location', 'category':'category'})

        response=self.client.get(TestReview.business+'/2/review')
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("No reviews found", response_msg["message"])

    def view_reviews_but_no_business_with_given_id(self):
        """Test if api cannot retrieve reviews when given business id does not exists"""
        response=self.client.get(TestReview.business+'/3/review')
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("No business with the given id", response_msg["message"])

    def tearDown(self):
        """clear all test variables."""
        with self.app.app_context():
            "Delete all tables"
            db.session.remove()
            db.drop_all()