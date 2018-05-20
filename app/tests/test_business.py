import unittest
import os
import json
from app import create_app, db
 
class TestBusiness(unittest.TestCase):
    def setUp(self):
        """Initialize our test app with Testing configuration"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        """data for testing our app"""
       
        self.business = {'business_name':'Andela', 'about':'Software Dev', 'location':'TRM', 'category':'Technology'}
        with self.app.app_context():
            db.create_all()

    """ Endpoints to test """

    register = '/api/v1/auth/register'
    login = '/api/v1/auth/login'
    business = '/api/v1/businesses'

    def register_user(self):
        """Register a test user"""
        return self.client.post(TestBusiness.register, data={'username':'kezzy', 'email':'user@email.com', 'password':'user_password', 'confirm_password':'user_password'})

    def login_user(self):
        """Login registered test user"""
        result = self.client.post(TestBusiness.login, data={ 'username':'kezzy','password':'user_password'})
        access_token = json.loads(result.data.decode())['access_token']
        return access_token

    def create_business(self):
        """ Create a test business """
        self.register_user()
        token = self.login_user()
        return self.client.post(TestBusiness.business, headers=dict(Authorization="Bearer " + token), data=self.business)

    def test_register_business(self): 
        """ Test if api can register a business"""
        res = self.create_business()
        self.assertEqual(res.status_code, 201)
        result = json.loads(res.data.decode('UTF-8'))
        self.assertEqual(result['Success'], 'Business Created successfully')

            
    def test_register_business_with_already_existing_business_name(self):
        """ Test if api can't register a business when the business name filled in is already registered"""
        self.create_business()
        res = self.create_business()
        
        self.assertEqual(res.status_code, 409)
        result = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Business already exists, use a different business name", result["Error"])  


    def test_register_business_with_incomplete_information(self):  
        """ Test if api can't register a business when any field has not been filled in """
        self.register_user()
        token = self.login_user()
        res = self.client.post(TestBusiness.business, headers=dict(Authorization="Bearer " + token), data={'business_name':'', 'about':'about', 'location':'location', 'category':'category'})
        self.assertEqual(res.status_code, 400) 
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Invalid input, kindly fill in all required input", response_msg['message'])  


    def test_register_business_with_white_space_inputs(self):  
        """ Test if api can't register a business when white spaces/tabs only are used as inputs """
        self.register_user()
        token = self.login_user()
        res = self.client.post(TestBusiness.business, headers=dict(Authorization="Bearer " + token), data={'business_name':'  ', 'about':'about', 'location':'location', 'category':'category'})
        self.assertEqual(res.status_code, 400) 
        response_msg = json.loads(res.data.decode("UTF-8"))
        self.assertEqual("Kindly input the missing fields", response_msg["Message"])  


    def test_get_all_businesses(self): 
        """Test if api can retrieve all businesses """ 
        self.create_business()
        response = self.client.get(TestBusiness.business)
        self.assertEqual(response.status_code, 200)



    def test_get_all_businesses_when_none_exists(self):
        """Test if api can show error when user tries to view businesses but no business is available """ 
        response = self.client.get(TestBusiness.business)
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("No Businesses Available", response_msg["Message"])

    def test_retrieve_a_business_by_id(self): 
        """ Test if api can retrieve a business by ID"""  
        self.create_business()
        response = self.client.get(TestBusiness.business+'/1')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_a_businesses_by_none_existing_id(self): 
        """ Test if api can display 'not found' error when business with the given ID is not found """        
        response = self.client.get(TestBusiness.business+'/1')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('No Business with that ID', response_msg['Error'])   
    
    def test_search_business_by_name(self): 
        """Test if api can search business by name""" 
        self.create_business()
        response = self.client.get(TestBusiness.business+'?q=Andela')
        self.assertEqual(response.status_code, 200)

    def test_search_business_by_non_existing_business_name(self): 
        """Test if api can display 'not found' error when seach by name gets no matching business """ 
        self.create_business()
        response = self.client.get(TestBusiness.business+'?q=Classy')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Sorry, No business with that name", response_msg["message"])

    def test_retrieve_businesses_in_a_specific_location(self): 
        """Test if api can display businesses in a given location""" 
        self.create_business()
        response = self.client.get(TestBusiness.business+'?location=TRM')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_businesses_in_a_location_with_no_registered_businesses(self): 
        """Test if api can display 'not found' error when no business is found in the given search location """ 
        self.create_business()
        response = self.client.get(TestBusiness.business+'?location=Classy')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Sorry, No business in that location", response_msg["Message"])

    def test_retrieve_businesses_in_a_specific_category(self): 
        """Test if api can display businesses in a given category """ 
        self.create_business()
        response = self.client.get(TestBusiness.business+'?category=Tech')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_businesses_of_a_category_with_no_registered_businesses(self): 
        """Test if api can display 'not found' error when no business is found in the given category""" 
        self.create_business()
        response = self.client.get(TestBusiness.business+'?category=Classy')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Sorry, No business in that category", response_msg["Message"])

    def test_retrieve_my_businesses(self): 
        """Test if api can retrieve all businesses of the logged in user""" 
        self.register_user()
        token = self.login_user()
        self.client.post(TestBusiness.business, headers=dict(Authorization="Bearer " + token), data={'business_name':'my business', 'about':'about', 'location':'location', 'category':'category'})

        response = self.client.get('/api/v1/mybusinesses', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(response.status_code, 200)

    
    def test_update_business(self):
        """ Test if api can update a business """
        self.register_user()
        token = self.login_user()

        self.client.post(TestBusiness.business, headers=dict(Authorization="Bearer " + token), data=self.business)
        response = self.client.put(TestBusiness.business+'/1', headers=dict(Authorization="Bearer " + token), data={'business_name':'Andela Kenya', 'about':'Software Development', 'location':'TRM', 'category':'Technology'})
        
        self.assertEqual(response.status_code, 200)

    def test_update_business_with_incomplete_information(self):
        """ Test if api cannot update a business when some input fields are not filled """

        self.register_user()
        token = self.login_user()
        self.client.post(TestBusiness.business,headers=dict(Authorization="Bearer " + token), data=self.business)
        
        response = self.client.put(TestBusiness.business+'/1',headers=dict(Authorization="Bearer " + token), data={'business_name':'', 'about':'Software Development', 'location':'TRM', 'category':'Technology'})
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('Invalid input, kindly fill in all required input', response_msg['message'])

    def test_update_business_with_non_existent_id(self):
        """ Test if api cannot update a business when no business of the given id exists """

        self.register_user()
        token = self.login_user()
        
        response = self.client.put(TestBusiness.business+'/1',headers=dict(Authorization="Bearer " + token), data={'business_name':'Andela', 'about':'Software Development', 'location':'TRM', 'category':'Technology'})
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual('You have no business with that ID', response_msg['Message'])
        

    def test_delete_business(self):
        """ Test if api can delete a business """   

        self.register_user()
        token = self.login_user()

        self.client.post(TestBusiness.business, headers=dict(Authorization="Bearer " + token), data=self.business)
        response_delete = self.client.delete(TestBusiness.business+'/1', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(response_delete.status_code, 200)

    def test_delete_non_existing_business(self):
        """ Test if api cannot delete a non existing business """

        self.register_user()
        token = self.login_user()

        result = self.client.delete(TestBusiness.business+'/100', headers=dict(Authorization="Bearer " + token))
        self.assertEqual(result.status_code, 404)
        result_msg = json.loads(result.data.decode("UTF-8"))
        self.assertEqual("You have no business with that ID", result_msg["Error"])


        
    def tearDown(self):
        """clear all test variables."""
        with self.app.app_context():
            "Delete all tables"
            db.session.remove()
            db.drop_all()