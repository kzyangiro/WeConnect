import jwt
from datetime import datetime, timedelta
from flask import current_app


class Business(object):
    """Business Class Creates an instance of business"""
    business_list = []
    
    def __init__(self, business_name, about, location, category):
        self.businessid=len(Business.business_list)+1
        self.business_name = business_name
        self.location=location
        self.about=about
        self.category=category
        self.created_by=category
        self.reviews= []


    def save(self, instance):
        """ This method adds the instance of the business created into business_List"""
        return Business.business_list.append(instance)


class User(object):
    """User class creates an instance of a user"""
    USERS = []
    def __init__(self, username, email, password):
        self.userid=len(User.USERS)+1
        self.username = username
        self.email=email
        self.password=password

    def save(self,instance):
        """Save method adds the created users details into the users list"""
        User.USERS.append(instance)

    @staticmethod
    def get_all():
        return User.query.all()

    def generate_token(self, user_id):
        """ This method generates the token to be used for authentification, returns a string"""

        try:
            """set payload, and indicate expiry duration of the token"""
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            """create the byte string token"""
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )

            jwt_string1 = jwt_string.decode("utf-8")
            return jwt_string1

        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token"""
        try:
            """Use SECRET variable used in configuration to decode token"""
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:            
            return "Kindly login to get a new token. Access Token is Expired"

        except jwt.InvalidTokenError:
            return "Please register or login, Invalid Token"
class BlacklistToken(object):
    """List for storing blacklisted JWT tokens"""
    blacklist_tokens = []


    def __init__(self, token):
        self.id=len(BlacklistToken.blacklist_tokens)+1
        self.token = token
        
class Review(object):
    """Reviews class creates an instance of a review"""
    reviews=[]

    def __init__(self, title, content):

        self.id=len(Review.reviews)+1
        self.title = title
        self.content = content






