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
        self.business1 = {'business_name':'', 'about':'about', 'location':'location'}

 
    def test_register_business(self):        
        response = self.client.post('/api/businesses', data=self.business)
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("business added successfully", response_msg["message"])

    def test_replication_business(self):        
        response = self.client.post('/api/businesses', data=self.business)
        self.assertEqual(response.status_code, 201) 
        response2 = self.client.post('/api/businesses', data=self.business)
        response_msg = json.loads(response2.data.decode("UTF-8"))
        self.assertEqual(response2.status_code, 503)
        self.assertEqual("business already exists", response_msg["message"])  

    def test_incomplete_business_information(self):        
        response = self.client.post('/api/businesses', data=self.business1)
        self.assertEqual(response.status_code, 404) #sta 
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("incomplete information", response_msg["message"])  


    def test_retrieve_all_businesses(self):        
        response = self.client.post('/api/businesses', data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/businesses')
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Available Businesses", response_msg["message"])

    def test_retrieve_all_businesses_when_none_exists(self):
        response = self.client.get('/api/businesses')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("No businesses found", response_msg["message"])

    def test_retrieve_a_businesses_by_id(self):        
        response = self.client.post('/api/businesses', data=self.business)
        self.assertEqual(response.status_code, 201)

        get_response = self.client.get('/api/businesses')
        response_msg_get = json.loads(get_response.data.decode("UTF-8")) 
        response_get_by_id = self.client.get('/api/businesses/{}'.format(response_msg_get['businesses']['my business']))

        self.assertEqual(response_get_by_id.status_code, 200)

    def test_retrieve_a_businesses_by_none_existing_id(self):        
        response = self.client.post('/api/businesses', data=self.business)
        response = self.client.get('/api/businesses/100')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Business not found:", response_msg["message"])

    def test_retrieve_a_businesses_by_none_existing_id_when_no_business_available(self): 
        response = self.client.get('/api/businesses/100')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("No businesses available", response_msg["message"])        


    def test_update_business(self):        
        response = self.client.post('/api/businesses', data={"business_name":"Andela", "location":"location", "about":"about", "contacts":"contacts"})
        self.assertEqual(response.status_code, 201)
        response = self.client.put('/api/businesses/1',  data={"business_name":"Andela Kenya", "location":"Kenya", "about":"about", "contacts":"contacts"})
        self.assertEqual(response.status_code, 200)
    
    def test_update_business_by_none_existing_id(self):
        response = self.client.put('/api/businesses/100hjjgghs',  data={"business_name":"Andela Kenya", "location":"Kenya", "about":"about", "contacts":"contacts"})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Business not found", response_msg["message"])

    def test_delete_business(self):        
        result = self.client.post('/api/businesses', data=self.business)
        self.assertEqual(result.status_code, 201)
        get_response = self.client.get('/api/businesses')
        response_msg_get = json.loads(get_response.data.decode("UTF-8")) 
        response_delete = self.client.delete('/api/businesses/{}'.format(response_msg_get['businesses']['my business']))
        self.assertEqual(response_delete.status_code, 204)

    def test_delete_business_by_none_existing_id(self):
        result = self.client.delete('/api/businesses/100')
        self.assertEqual(result.status_code, 404)
        result_msg = json.loads(result.data.decode("UTF-8"))
        self.assertIn("The business not found", result_msg["message"])

    #Clear my list

    def tearDown(self):
        Business.business_list=[]
        
