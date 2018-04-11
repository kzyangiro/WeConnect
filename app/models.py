from app import db
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from flask import current_app


class User(db.Model):
    """User class creates an instance of a user"""
    #user = []
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

        #Hash password
        self.password = Bcrypt().generate_password_hash(password).decode('utf-8')

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

        
    def save(self):
        """Save method adds the created users details into the users list"""

        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def generate_token(self, user_id):
        """ This method generates the token to be used for authentification"""

        try:
            #set payload, and indicate expiry duration of the token
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

class Business(db.Model): #This class represents the Businesses Table
    """Business Class Creates an instance of business"""
    #business_list = []
    __tablename__ = 'businesses'

    businessid = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(255))
    location = db.Column(db.String(255))
    about = db.Column(db.String(255))
    category = db.Column(db.String(255))

    #store modification timestamps
    
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
        #return Business.business_list.append(instance)

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




class Review(db.Model):
    """Reviews class creates an instance of a review"""
    #reviews=[]
    __tablename__ ='reviews'

    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(255))
    content=db.Column(db.String(255))
    
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    #store modification timestamps
    
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
    db.DateTime, default=db.func.current_timestamp(),
    onupdate = db.func.current_timestamp())


    businessid = db.Column(db.Integer, db.ForeignKey(Business.businessid))

    def __init__(self, title, content, created_by, businessid):

        self.title = title
        self.content = content
        self.created_by = created_by
        self.businessid = businessid

 
    def save(self):
        """ This method adds the instance of the review created into reviews table"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(businessid):
        """ This method retrieves all the reviews of a business"""
        return Review.query.filter_by(businessid = businessid)
        