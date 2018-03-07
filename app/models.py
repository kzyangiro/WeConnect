import uuid

class Business(object):
    business_list = []
    
    def __init__(self, business_name, about, location, contacts):
        self.businessid=str(uuid.uuid4())
        self.business_name = business_name
        self.location=location
        self.about=about
        self.contacts=contacts


    def save(self, instance):
        Business.business_list.append(instance)

    def get_all(self):
        return Business.business_list

    def delete(self):
        return Business.business_list.remove(self)

class User(object):
    pass

class Review(object):
    pass


