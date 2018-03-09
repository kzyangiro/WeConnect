#import uuid

class Business(object):
    business_list = []
    
    def __init__(self, business_name, about, location, category):
        self.businessid=len(Business.business_list)+1
        #self.businessid=str(uuid.uuid4())
        self.business_name = business_name
        self.location=location
        self.about=about
        self.category=category
        self.reviews= []


    def save(self, instance):
        Business.business_list.append(instance)

    def get_all(self):
        return Business.business_list

    def delete(self):
        return Business.business_list.remove(self)

class User(object):
    user = []
    def __init__(self, username, email, password):
        self.userid=len(User.user)+1
        self.username = username
        self.email=email
        self.password=password

    def save(self,instance):
        User.user.append(instance)

class Review(object):
    reviews=[]

    def __init__(self, title, content):

        self.id=len(Review.reviews)+1
        self.title = title
        self.content = content
        


