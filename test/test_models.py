import unittest
from app.models import Users
 
class TestUserClass(unittest.TestCase):
    def setUp():
        self.user = User()
 
    def test_create_user(self):        
        response = self.user.create_user("fullname","username", "email", "password")
        self.assertEqual(response["message"], "User Created Successfully")
 
 
if __name__ == '__main__':
    unittest.main()