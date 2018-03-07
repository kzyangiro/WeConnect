import unittest
import os
import json
from app import create_app
from app.models import Business
 
class TestBusinessClass(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.business = {'business_name':'my business', 'about':'about', 'location':'location'}
 
    def test_register_business(self):        
        response = self.client.post('/api/businesses', data=self.business)
        self.assertEqual(response.status_code, 201)
        

    def test_retrieve_all_businesses(self):        
        response = self.client.post('/api/businesses', data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/businesses')
        self.assertEqual(response.status_code, 301)

    def test_retrieve_a_businesses_by_id(self):        
        response = self.client.post('/api/businesses', data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/businesses/1')
        self.assertEqual(response.status_code, 301)


    def test_update_business(self):        
        response = self.client.post('/api/businesses', data={"business_name":"Andela", "location":"location", "about":"about", "contacts":"contacts"})
        self.assertEqual(response.status_code, 201)
        response = self.client.put('/api/businesses/1',  data={"business_name":"Andela Kenya", "location":"Kenya", "about":"about", "contacts":"contacts"})
        self.assertEqual(response.status_code, 200)
    
    def test_delete_business(self):        
        response = self.client.post('/api/businesses', data=self.business)
        self.assertEqual(response.status_code, 201)
        result = self.client.delete('/api/businesses/1')
        self.assertEqual(result.status_code, 200)
        #Check if exists, return not found
        result = self.client.get('/api/businesses/1')
        self.assertEqual(result.status_code, 301)

    #Clear my list

    def tearDown(self):
        Business.business_list=[]
        
