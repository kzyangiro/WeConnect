from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from flask import request, current_app


class User(db.Model):
    """User class creates an instance of a user"""
 
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    businesses = db.relationship(
        'Business', order_by='Business.businessid', cascade="all, delete-orphan")

    reviews = db.relationship(
        'Review', order_by='Review.id', cascade="all, delete-orphan")


    def __init__(self, username, email, password):
         
        self.username = username
        self.email=email

        """Hash password"""
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')

    def password_is_valid(self, password):
        """
        Checks if provided password matches the hashed stored password
        """
        return Bcrypt().check_password_hash(self.password, password)

        
    def save(self):
        """Add the created users details into the users table"""

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def generate_token(self, user_id):
        """ This method generates the token to be used for authentification"""

        try:
            """set payload, and indicate expiry duration of the token"""
            payload = {
                # datetime.utcnow()
                'exp': datetime.now() + timedelta(minutes=5),
                'iat': datetime.now(),
                'sub': user_id
            }
            """create the token"""
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            return str(e)

        
    @staticmethod
    def get_token():

        auth_header = request.headers.get('Authorization')

        if auth_header:
            access_token = auth_header.split(' ')[1]
        else:
            access_token = 'Invalid Token'
        return access_token

    @staticmethod
    def validate_token():
        """ Check if token used is valid"""

        access_token = User.get_token()
        user_id = User.decode_token(access_token)
        blacklisttoken = BlacklistToken.query.filter_by(
                token=access_token).first()

        res = {'access_token':User.get_token(),
            'user_id': User.decode_token(access_token),
            'decodable_token':access_token and isinstance(user_id, str),
            'blacklisted_token':access_token and blacklisttoken}
        return res



    @staticmethod
    def decode_token(token):
        """Decodes the access token"""
        try:
            """Use SECRET variable used in configuration to decode token"""
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:            
            return "Kindly login to get a new token. Token is Expired"

        except jwt.InvalidTokenError:
            return "Please register or login, Token is Invalid"

class BlacklistToken(db.Model):
    """User class creates an instance of a user"""
 
    __tablename__ = 'blacklist'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(), nullable=False)


    def __init__(self,token):
         
        self.token = token
        
    def save(self):
        """Add the token details into the blacklists table"""

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return BlacklistToken.query.all()



class Business(db.Model): 
    """Business Class Creates an instance of business"""
    __tablename__ = 'businesses'

    businessid = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    about = db.Column(db.String(255))
    category = db.Column(db.String(255))

    """store modification timestamps"""
    
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
    db.DateTime, default=db.func.current_timestamp(),
    onupdate = db.func.current_timestamp())

    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    
    def __init__(self,business_name, about, location, category, created_by):

        self.business_name = business_name
        self.location=location
        self.about=about
        self.category=category
        self.reviews= []

        #Save user who has created the business

        self.created_by = created_by


    def save(self):
        """ This method adds the instance of the business created into businesses table"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all_auth(user_id):
        """ This method retrieves all busineses for the particular logged in user"""

        return Business.query.filter_by(created_by = user_id)

    @staticmethod
    def get_all():
        """ This method retrieves all busineses"""
        return Business.query.all()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        #method represents the object instance of the model whenever it is queries.
        return "<Business: {}>".format(self.business_name)


    @property
    def serialize(self):
        """Serialize."""
        obj = {
            "Business id":self.businessid,
            "Business Name":self.business_name,
            "Category":self.category,
            "Business location":self.location
        }

        return obj


class Review(db.Model):
    """Reviews class creates an instance of a review"""
   
    __tablename__ ='reviews'

    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(255))
    
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    #store modification timestamps
    
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
    db.DateTime, default=db.func.current_timestamp(),
    onupdate = db.func.current_timestamp())


    businessid = db.Column(db.Integer, db.ForeignKey(Business.businessid))

    def __init__(self, content, created_by, businessid):

        self.content = content
        self.created_by = created_by
        self.businessid = businessid

 
    def save(self):
        """ This method adds the instance of the review created into reviews table"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()        

    @staticmethod
    def get_all(businessid):
        """ This method retrieves all the reviews of a business"""
        return Review.query.filter_by(businessid = businessid)
