class Business(object):
    """Business Class Creates an instance of business"""
    business_list = []
    
    def __init__(self, business_name, about, location, category):
        self.businessid=len(Business.business_list)+1
        self.business_name = business_name
        self.location=location
        self.about=about
        self.category=category
        self.reviews= []


    def save(self, instance):
        """ This method adds the instance of the business created into business_List"""
        return Business.business_list.append(instance)


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
        


