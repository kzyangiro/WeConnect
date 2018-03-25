import unittest
import os
import json
from app import create_app
from app.models import Business
 
class TestBusinessClass(unittest.TestCase):
    def setUp(self):
        """Initialize our test app with Testing configuration"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        """data for testing our app"""
        self.business = {'business_name':'my business', 'about':'about', 'location':'location', 'category':'category'}
        self.business1 = {'business_name':'', 'about':'about', 'location':'location', 'category':'category'}
        self.new_business = {'business_name':'hemstar', 'about':'about', 'location':'location', 'category':'category'}

 
    def test_register_business(self): 
        """Tests if the api can create a business"""       
        response = self.client.post('/api/v1/businesses', data=self.business)
        if self.business["business_name"] and self.business["about"] and self.business["location"] and self.business["category"]:
            self.assertEqual(response.status_code, 201)
            response_msg = json.loads(response.data.decode("UTF-8"))
            self.assertEqual("Business created successfully", response_msg["Message"])
            
    def test_no_replication_of_business(self):
        """Tests if no dublicate business names are allowed"""       
        response = self.client.post('/api/v1/businesses', data=self.business)
        self.assertEqual(response.status_code, 201) 
        response2 = self.client.post('/api/v1/businesses', data=self.business)
        response_msg = json.loads(response2.data.decode("UTF-8"))
        self.assertEqual(response2.status_code, 409)
        self.assertEqual("Business already exists", response_msg["message"])  

    def test_incomplete_business_information(self):        
        """Tests if a business cannot be created with some fields empty"""
        response = self.client.post('/api/v1/businesses', data=self.business1)
        self.assertEqual(response.status_code, 400) #sta 
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Incomplete information", response_msg["message"])  


    def test_retrieve_all_businesses(self): 
        """Tests if businesses can be retrieved"""       
        response = self.client.post('/api/v1/businesses', data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/businesses')
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Available Businesses:", response_msg["Message"])

    def test_retrieve_all_businesses_when_none_exists(self):
        response = self.client.get('/api/v1/businesses')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("No businesses found", response_msg["message"])

    def test_retrieve_a_businesses_by_id(self):        
        response = self.client.post('/api/v1/businesses', data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/businesses/1')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_a_businesses_by_none_existing_id(self):        
        response = self.client.post('/api/v1/businesses', data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/businesses/100')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('No Business with the given ID', response_msg['message'])

    def test_retrieve_a_businesses_by_none_existing_id_when_no_business_available(self):
        response = self.client.get('/api/v1/businesses/40')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("No businesses available", response_msg["message"])        
    
    
    def test_update_business(self):
        self.client.post('/api/v1/businesses', data=self.business)
        response = self.client.put('/api/v1/businesses/1', data=self.new_business)
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('Business Updated Successfully', response_msg['message'])

    def test_update_business_with_incomplete_information(self):
        self.client.post('/api/v1/businesses', data=self.business)
        response = self.client.put('/api/v1/businesses/1', data=self.business1)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('Fill in the Empty fields', response_msg['message'])

    def test_update_business_with_non_existent_id(self):
        self.client.post('/api/v1/businesses', data=self.business)
        response = self.client.put('/api/v1/businesses/160', data=self.business)
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('Business not found', response_msg['message'])
        

    def test_delete_business(self):        
        response = self.client.post('/api/v1/businesses', data=self.business)
        self.assertEqual(response.status_code, 201)
        response_delete = self.client.delete('/api/v1/businesses/1')
        self.assertEqual(response_delete.status_code, 200)
        # response_msg = json.loads(response_delete.data.decode("UTF-8"))
        # self.assertEqual('Business Deleted Successfully', response_msg['message'])

    def test_delete_business_by_none_existing_id(self):
        result = self.client.delete('/api/v1/businesses/100')
        self.assertEqual(result.status_code, 404)
        # result_msg = json.loads(result.data.decode("UTF-8"))
        # self.assertEqual("No Business with that ID", result_msg["message"])

    def test_delete_with_no_business(self): 
        response_delete = self.client.delete('/api/v1/businesses/1')
        self.assertEqual(response_delete.status_code, 404)
        response_msg = json.loads(response_delete.data.decode("UTF-8"))
        self.assertIn('No Business Found', response_msg['message'])


    def tearDown(self):
        """Method to clear business_list when testing is completed"""
        Business.business_list=[]
        
