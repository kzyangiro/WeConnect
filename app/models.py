from app import db

class Business(db.Model):
    """Business Class Creates an instance of business"""
    #business_list = []
    __tablename__ = 'businesses'

    businessid = db.Column(db.Integer)
    business_name = db.Column(db.String(255), primary_key=True)
    location = db.Column(db.String(255))
    about = db.Column(db.String(255))
    category = db.Column(db.String(255))
    

    
    def __init__(self, business_name, about, location, category):
        self.businessid=len(Business.business_list)+1
        self.business_name = business_name
        self.location=location
        self.about=about
        self.category=category
        self.reviews= []


    def save(self, instance):
        """ This method adds the instance of the business created into businesses table"""
        db.session.add(self)
        db.session.commit()
        #return Business.business_list.append(instance)

    @staticmethod
    def get_all(self):
        return Business.query.all(self)
        
    @staticmethod
    def delete(self):
        db.session.delete(self)

    



class User(object):
    """User class creates an instance of a user"""
    user = []
    def __init__(self, username, email, password):
        self.userid=len(User.user)+1
        self.username = username
        self.email=email
        self.password=password

    def save(self,instance):
        """Save method adds the created users details into the users list"""
        User.user.append(instance)

class Review(object):
    """Reviews class creates an instance of a review"""
    reviews=[]

    def __init__(self, title, content):

        self.id=len(Review.reviews)+1
        self.title = title
        self.content = content
        


