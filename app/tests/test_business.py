import unittest
import os
import json
from app import create_app, db
 
class TestBusinessClass(unittest.TestCase):
    def setUp(self):
        """Initialize our test app with Testing configuration"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        """data for testing our app"""
        self.user_data = {'username':'kezzy', 'email':'user@email.com', 'password':'user_password', 'confirm_password':'user_password'}
        self.user_login_data = { 'username':'kezzy','password':'user_password'}
        self.business = {'business_name':'my business', 'about':'about', 'location':'location', 'category':'category'}
        self.business1 = {'business_name':'', 'about':'about', 'location':'location', 'category':'category'}
        self.business2 = {'business_name':'  ', 'about':'about', 'location':'location', 'category':'category'}
        self.new_business = {'business_name':'hemstar', 'about':'about', 'location':'location', 'category':'category'}

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    #To register a business, we need to have an registered user login
    def register_user(self):
        """Register a test user"""
        return self.client.post('/api/v1/auth/register', data=self.user_data)

    def login_user(self):
        """Test user to login"""
        return self.client.post('/api/v1/auth/login', data=self.user_login_data)


    def test_register_business(self): 
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        """Tests if the api can create a business"""       
        res = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['Success'], 'Business Created successfully')

            
    def test_no_replication_of_business(self):
        """ User has to be registered and logged in """
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        """Tests if no dublicate business names are allowed"""       
        response = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(response.status_code, 201) 
        response2 = self.client.post('/api/v1/businesses',headers=dict(Authorization="Bearer " + access_token), data=self.business)
        response_msg = json.loads(response2.data.decode("UTF-8"))
        self.assertEqual(response2.status_code, 409)
        self.assertEqual("Business already exists, use a different business name", response_msg["Error"])  


    def test_incomplete_business_information(self):  
        """ User has to be registered and logged in """
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        """Tests if a business cannot be created with some fields empty"""
        response = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token),data=self.business1)
        self.assertEqual(response.status_code, 400) 
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Invalid input, kindly fill in all required input", response_msg["message"])  
 
    def test_empty_spaces_inputs(self):  
        """ User has to be registered and logged in """
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        """Tests if a business cannot be created with some fields empty"""
        response = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token),data=self.business2)
        self.assertEqual(response.status_code, 400) 
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Kindly input the missing fields", response_msg["Message"])  


    def test_retrieve_all_businesses(self): 
        """Tests if all businesses can be retrieved""" 
        self.register_user()
        result = self.login_user()    

        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/businesses')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_my_businesses(self): 
        """Tests if all a logged in user can retrieve his registered businesses""" 
        self.register_user()
        result = self.login_user()    

        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/mybusinesses', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_non_existent_businesses_by_name(self): 
        """Tests if all a logged in user can retrieve his registered businesses""" 
        self.register_user()
        result = self.login_user()    

        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/businesses?q=Classy')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Sorry, No business with that name", response_msg["message"])

    def test_retrieve_non_existent_businesses_in_location(self): 
        """Tests if all a logged in user can retrieve his registered businesses""" 
        self.register_user()
        result = self.login_user()    

        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/businesses?location=Classy')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Sorry, No business in that location", response_msg["Message"])


    def test_retrieve_non_existent_businesses_in_category(self): 
        """Tests if all a logged in user can retrieve his registered businesses""" 
        self.register_user()
        result = self.login_user()    

        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/businesses?category=Classy')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Sorry, No business in that category", response_msg["Message"])


    def test_retrieve_all_businesses_when_none_exists(self):
        response = self.client.get('/api/v1/businesses')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("No Businesses Available", response_msg["Message"])

    def test_retrieve_a_businesses_by_id(self):   
        self.register_user()
        result=self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post('/api/v1/businesses',headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(response.status_code, 201)
        response = self.client.get('/api/v1/businesses/1')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_a_businesses_by_none_existing_id(self):        
        response = self.client.get('/api/v1/businesses/100')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('No Business with that ID', response_msg['Error'])   
    
    
    def test_update_business(self):
        self.register_user()
        result=self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post('/api/v1/businesses',headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(response.status_code, 201)
        
        response = self.client.put('/api/v1/businesses/1', headers=dict(Authorization="Bearer " + access_token), data=self.new_business)
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('Business updated successfully', response_msg['Success'])

    def test_update_business_with_incomplete_information(self):

        self.register_user()
        result=self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post('/api/v1/businesses',headers=dict(Authorization="Bearer " + access_token), data=self.business)
        self.assertEqual(response.status_code, 201)

        response = self.client.put('/api/v1/businesses/1',headers=dict(Authorization="Bearer " + access_token), data=self.business1)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('Fill in the empty fields', response_msg['message'])

    def test_update_business_with_non_existent_id(self):

        self.register_user()
        result=self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.put('/api/v1/businesses/160', headers=dict(Authorization="Bearer " + access_token),data=self.business)
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual('No Business with that ID', response_msg['Message'])
        

    def test_delete_business(self):   

        self.register_user()
        result=self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        response_delete = self.client.delete('/api/v1/businesses/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response_delete.status_code, 200)

    def test_delete_non_existing_business(self):

        self.register_user()
        result=self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        result = self.client.delete('/api/v1/businesses/100', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)
        result_msg = json.loads(result.data.decode("UTF-8"))
        self.assertEqual("No Business with that ID", result_msg["Error"])


        
