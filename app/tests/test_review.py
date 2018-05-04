import unittest, os, json
from app import create_app
from app.models import Review, Business
 
class TestReviewClass(unittest.TestCase):
    """Class for testing review model"""
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        """data for testing"""
        self.user_data = {'username':'kezzy', 'email':'user@email.com', 'password':'user_password', 'confirm_password':'user_password'}
        self.user_login_data = { 'username':'kezzy','password':'user_password'}
        self.reviews = {'title':'my review', 'content':'my reviews content'}
        self.reviews1 = {'title':'', 'content':'my reviews content'}
        self.business = {'business_name':'my business', 'about':'about', 'location':'location', 'category':'category'}
        self.business1 = {'business_name':'my new business', 'about':'about', 'location':'location', 'category':'category'}

    #Adding a review requires authentication
    def register_user(self):
        """Register a test user"""
        return self.client.post('/api/v1/auth/register', data=self.user_data)

    def login_user(self):
        """Test user to login"""
        return self.client.post('/api/v1/auth/login', data=self.user_login_data)

    def test_create_review(self):
        """Test if review is created"""
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        
        response=self.client.post('/api/v1/businesses/1/review', headers=dict(Authorization="Bearer " + access_token), data = self.reviews)
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Review added successfully", response_msg["message"])


    def test_no_business_with_given_id(self):
        """Test if business id indicated does not exist"""
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        
        response=self.client.post('/api/v1/businesses/3/review', headers=dict(Authorization="Bearer " + access_token), data = self.reviews)
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual('No business with the given id', response_msg["message"])


    def test_incomplete_information(self):
        """Test if title or content is not filled in"""
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        
        response=self.client.post('/api/v1/businesses/1/review', headers=dict(Authorization="Bearer " + access_token), data = self.reviews1)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual('Incomplete Information', response_msg["message"])

    def test_invalid_token(self):
        """Test if user is creating a review with an invalid token"""
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        
        response=self.client.post('/api/v1/businesses/3/review', data = self.reviews)
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual('Invalid token, Login to obtain a new token', response_msg["message"])

    def test_view_reviews(self):
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        
        self.client.post('/api/v1/businesses/1/review', headers=dict(Authorization="Bearer " + access_token), data = self.reviews)
        response=self.client.get('/api/v1/businesses/1/review')
        self.assertEqual(response.status_code, 200)


    def tearDown(self):
        Review.reviews=[]
