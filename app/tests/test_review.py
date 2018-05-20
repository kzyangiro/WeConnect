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

        #Testing data
        self.business = {'business_name':'my business', 'about':'about', 'location':'location', 'category':'category'}
        
        with self.app.app_context():
            db.create_all()

    """ Endpoints to test """

    register = '/api/v1/auth/register'
    login = '/api/v1/auth/login'
    business = '/api/v1/businesses'

    def register_user(self):
        """Register a test user"""
        return self.client.post(TestReview.register, data={'username':'kezzy', 'email':'user@email.com', 'password':'user_password', 'confirm_password':'user_password'})

    def login_user(self):
        """Login registered test user"""
        result = self.client.post(TestReview.login, data={ 'username':'kezzy','password':'user_password'})
        access_token = json.loads(result.data.decode())['access_token']
        return access_token

    def create_business_review(self):
        """ Create a test business """
        self.register_user()
        token = self.login_user()
        self.client.post(TestReview.business, headers=dict(Authorization="Bearer " + token), data=self.business)

        response=self.client.post(TestReview.business+'/1/review', headers=dict(Authorization="Bearer " + token), data = {'content':'my reviews content'})
        return response

    def test_creating_a_review_when_there_is_no_existing_businesses(self):
        """Test if review is not created if no business is available"""
        self.register_user()
        token = self.login_user()

        response=self.client.post(TestReview.business+'/1/review', headers=dict(Authorization="Bearer " + token), data = {'content':'my reviews content'})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("No business available", response_msg["message"])

    def test_creating_a_review_when_there_is_no_business_of_the_given_id(self):
        """Test if review is not created if business of id indicated does not exist"""
        self.register_user()
        token = self.login_user()
        self.client.post(TestReview.business, headers=dict(Authorization="Bearer " + token), data=self.business)


        response=self.client.post(TestReview.business+'/10/review', headers=dict(Authorization="Bearer " + token), data = {'content':'my reviews content'})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("No business with the given id", response_msg["message"])
        
        
    def test_create_review_with_incomplete_info(self):
        """Test if review is not created with incomplete information"""
        self.register_user()
        token = self.login_user()
        self.client.post(TestReview.business, headers=dict(Authorization="Bearer " + token), data=self.business)


        response=self.client.post(TestReview.business+'/1/review', headers=dict(Authorization="Bearer " + token), data = {'content':''})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Invalid input, kindly fill in all required input", response_msg["message"])


    def test_create_a_review(self):
        """Test if api can create a review"""
        response = self.create_business_review()
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Review added successfully", response_msg["Message"])


    def test_view_reviews(self):
        """Test api can retrieve reviews"""
        self.create_business_review()
        response=self.client.get(TestReview.business+'/1/review')
        self.assertEqual(response.status_code, 200)

    def test_view_reviews_but_no_reviews_available_for_that_business(self):
        """Test api cannot  retrieve reviews when none exists"""
        self.register_user()
        token = self.login_user()
        self.client.post(TestReview.business, headers=dict(Authorization="Bearer " + token), data=self.business)

        response=self.client.get(TestReview.business+'/1/review')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("No reviews found", response_msg["message"])

    def view_reviews_but_no_business_with_given_id(self):
        """Test api cannot retrieve reviews when given business id does not exists"""
        response=self.client.get(TestReview.business+'/1/review')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("No business with the given id", response_msg["message"])

    def tearDown(self):
        """clear all test variables."""
        with self.app.app_context():
            "Delete all tables"
            db.session.remove()
            db.drop_all()