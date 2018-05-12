import unittest, os, json
from app import create_app
from app.models import Business
 
class TestBusinessClass(unittest.TestCase):
    """Class for testing business model"""
    def setUp(self):
        """Initialize our test app with Testing configuration"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        """data for testing"""
        
        self.user_data = {'username':'kezzy', 'email':'user@email.com', 'password':'user_password', 'confirm_password':'user_password'}
        self.user_login_data = { 'username':'kezzy','password':'user_password'}

        
        self.business = {'business_name':'my business', 'about':'about', 'location':'location', 'category':'category'}
        self.business1 = {'business_name':'', 'about':'about', 'location':'location', 'category':'category'}
        self.new_business = {'business_name':'hemstar', 'about':'about', 'location':'location', 'category':'category'}

    #Adding, deleting and editing a business requires authentication
    def register_user(self):
        """Register a test user"""
        return self.client.post('/api/v1/auth/register', data=self.user_data)

    def login_user(self):
        """Test user to login"""
        return self.client.post('/api/v1/auth/login', data=self.user_login_data)
 
    def test_register_business(self): 
        """Tests if the api can create a business"""       
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        
        self.assertEqual(response.status_code, 201)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Business created successfully", response_msg["Message"])
            

    def test_no_replication_of_business(self):
        """Tests if no dublicate business names are allowed"""       
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        response = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        
        self.assertEqual(response.status_code, 409)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Business already exists", response_msg["message"])  

    def test_incomplete_business_information(self):        
        """Tests if a business cannot be created with some fields empty"""
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business1)
        
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Fill in the empty fields", response_msg["message"])   

    def test_register_business_with_invalid_token(self):        
        """Tests if a business cannot be created with some fields empty"""
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        response = self.client.post('/api/v1/businesses', data=self.business)
        
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("Invalid token, Login to obtain a new token", response_msg["message"]) 

    def test_retrieve_all_businesses(self): 
        """Tests if businesses can be retrieved"""       
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        
        response = self.client.get('/api/v1/businesses')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_all_businesses_when_none_exists(self):
        response = self.client.get('/api/v1/businesses')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("No Businesses Found", response_msg["message"])

    def test_retrieve_a_businesses_by_id(self):        
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        
        response = self.client.get('/api/v1/businesses/1')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_a_businesses_by_none_existing_id(self):        
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)
        
        response = self.client.get('/api/v1/businesses/100')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual('No Business with that ID', response_msg['message'])

    def test_retrieve_a_businesses_with_id_when_no_business_available(self):
        response = self.client.get('/api/v1/businesses/40')
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertEqual("No businesses found", response_msg["message"])        
    
    
    def test_update_business(self):

        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)

        response = self.client.put('/api/v1/businesses/1', headers=dict(Authorization="Bearer " + access_token), data=self.new_business)
        self.assertEqual(response.status_code, 200)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('Business Updated Successfully', response_msg['message'])

    def test_Invalid_token_update_business(self):

        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)

        response = self.client.put('/api/v1/businesses/1', data=self.new_business)
        self.assertEqual(response.status_code, 401)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('Invalid token, Login to obtain a new token', response_msg['message'])

    def test_update_non_existent_business(self):

        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)

        response = self.client.put('/api/v1/businesses/3', headers=dict(Authorization="Bearer " + access_token), data=self.new_business)
        self.assertEqual(response.status_code, 404)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('Business not found', response_msg['message'])

    def test_update_business_with_incomplete_information(self):
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)

        response = self.client.put('/api/v1/businesses/1', headers=dict(Authorization="Bearer " + access_token),data=self.business1)
        self.assertEqual(response.status_code, 400)
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn('Fill in the empty fields', response_msg['message'])
       

    def test_delete_business(self):        
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)

        response_delete = self.client.delete('/api/v1/businesses/1', headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response_delete.status_code, 200)
        response_msg = json.loads(response_delete.data.decode("UTF-8"))
        self.assertEqual('Business Deleted Successfully', response_msg['message'])

    def test_delete_business_by_none_existing_id(self):
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)

        result = self.client.delete('/api/v1/businesses/100', headers=dict(Authorization="Bearer " + access_token))
        
        self.assertEqual(result.status_code, 404)
        result_msg = json.loads(result.data.decode("UTF-8"))
        self.assertEqual("No Business with that ID", result_msg["message"])

    def test_delete_business_with_invalid_token(self):
        self.register_user()
        result = self.login_user()

        access_token = json.loads(result.data.decode())['access_token']

        self.client.post('/api/v1/businesses', headers=dict(Authorization="Bearer " + access_token), data=self.business)

        result = self.client.delete('/api/v1/businesses/1')
        
        self.assertEqual(result.status_code, 401)
        result_msg = json.loads(result.data.decode("UTF-8"))
        self.assertEqual('Invalid token, Login to obtain a new token', result_msg["message"])

    def test_unauthorised_user_delete_business(self):
        result = self.client.delete('/api/v1/businesses/1')
        
        self.assertEqual(result.status_code, 401)
        result_msg = json.loads(result.data.decode("UTF-8"))
        self.assertEqual('Invalid token, Login to obtain a new token', result_msg["message"])

    def tearDown(self):
        """Method to clear business_list when testing is completed"""
        Business.business_list=[]
        
