import unittest
import os
import json
from app import create_app
from app.models import Review
from app.models import Business
 
class TestReviewClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.reviews = {'title':'my review', 'content':'my reviews content'}
        self.reviews1 = {'title':'', 'content':'my reviews content'}
        self.reviews2 = {'title':'my review', 'content':''}
        self.business = {'business_name':'my business', 'about':'about', 'location':'location', 'category':'category'}

    # def test_business_exists(self):
    #     response1 = self.client.post('/api/v1/businesses', data=self.business)
    #     self.assertEqual(response1.status_code, 201)
    #     response = self.client.post('/api/v1/businesses/100/review', data=self.reviews)
    #     self.assertEqual(response.status_code, 404)
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     self.assertEqual("No business with the given id", response_msg["message"])

    # def test_no_title(self):
    #     response = self.client.post('/api/v1/businesses/1/review', data=self.reviews1)
    #     self.assertEqual(response.status_code, 400)
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     self.assertEqual("Incomplete Information", response_msg["message"])


    # def test_no_content(self):
    #     response = self.client.post('/api/v1/businesses/1/review', data=self.reviews2)
    #     self.assertEqual(response.status_code, 400)
    #     response_msg = json.loads(response.data.decode("UTF-8"))
    #     self.assertEqual("Incomplete Information", response_msg["message"])

    def test_review_created(self):
        """Test if review is created"""
        response1 = self.client.post('/api/v1/businesses', data=self.business)
        self.assertEqual(response1.status_code, 201)
        response=self.client.post('/api/v1/businesses/1/review', data = self.reviews)
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Review added successfully", response_msg["message"])

    def view_reviews(self):
        self.client.post('/api/v1/businesses', data=self.business)
        self.client.post('/api/v1/businesses/1/review', data = self.reviews)
        response=self.client.get('/api/v1/businesses/1/review')
        self.assertEqual(response.status_code, 302)
        

    def tearDown(self):
        Review.reviews=[]
