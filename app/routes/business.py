from flask import request, make_response, jsonify
from . import bs
from .. models import Business, User, BlacklistToken

@bs.route('/')
def homepage():
    """This is the home route"""
    return jsonify({'message':'Welcome to Weconnect'}), 200

@bs.route('/api/v1/businesses', methods=['POST'])
def register_business():
    """This method Creates a business by only authorised users"""
    

    business_name1 = request.data.get('business_name')
    about1 = request.data.get('about')
    location1 = request.data.get('location')
    category1 = request.data.get('category')


    """ Confirm user is authorised """
    auth_header = request.headers.get('Authorization')

    if auth_header:
        access_token = auth_header.split(' ')[1]
    else:
        access_token = 'Invalid Token'

    if access_token:

        for token in BlacklistToken.blacklist_tokens:
            "Check if input access token is blacklisted, if yes, prompt new login"
            if token == access_token:
                responce = make_response(jsonify({'status':'You are already Logged Out, kindly login first'}),400)
                return responce 
          

        """Decode token"""
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            
            try:

                if business_name1 and about1 and location1 and category1:

                    business_name = str(business_name1.strip(' '))
                    location = str(location1.strip(' '))
                    category = str(category1.strip(' '))
                    about = str(about1.strip(' '))
                else:
                    return jsonify({'message': "Fill in the empty fields"}), 400

                if business_name and about and location and category:

                    for business in Business.business_list:
                        if business.business_name == business_name:
                            """Ensure No duplicate entry of business name"""
                            return jsonify({'message':'Business already exists'}), 409

                    business = Business(business_name=business_name, about=about, location=location, category=category)

                    mybusinesses={'Business Name':business.business_name,'Description':business.about,'Location':business.location,'Category':business.category}

                    business.save(business)
                    response =make_response(
                        jsonify({
                            'business details': mybusinesses,
                            'Message':'Business created successfully'
                            }), 201)
                    return response
                else:
                    return jsonify({'message': "Fill in the empty fields"}), 400

            except Exception as e:
                return jsonify({'message': e}), 401
        else:
            return jsonify({'message': 'Invalid token, Login to obtain a new token'}), 401

            
@bs.route('/api/v1/businesses', methods=['GET'])
def retrieve_all_businesses():
    """This method retrieves all businesses"""
    results = []

    if len(Business.business_list) == 0:
        """ Checking if there is no business"""
        return jsonify({'message': "No Businesses Found"}), 404
        
    else:
        for business in Business.business_list:
            obj={
                "Business id":business.businessid,
                "Business name":business.business_name,
                "Category":business.category

            }
            results.append(obj)

        response=jsonify(results)
        response.status_code = 200
        return response

@bs.route('/api/v1/businesses/<int:businessid>', methods=['GET'])
def get_businesses_by_id(businessid):
    """This method retrieves a business by the given id"""
    
    if len(Business.business_list) == 0:
        return jsonify({'message': "No businesses found"}), 404

    else:
        
        for business in Business.business_list:
            if businessid == business.businessid:
                obj={
                    "Business Id":business.businessid,
                    "Business Name":business.business_name,
                    "Category":business.category,
                    "Business location":business.location,
                    "Description":business.about

                }
                response=jsonify(obj)
                response.status_code = 200
                return response

    return jsonify({"message":"No Business with that ID"}), 404


@bs.route('/api/v1/businesses/<int:businessid>', methods=['PUT'])
def update_businesses(businessid):

    """This method uses input data to update the content of a business of the ID indicated in the URL"""

    business_name1 = request.data.get('business_name')
    about1 = request.data.get('about')
    location1 = request.data.get('location')
    category1 = request.data.get('category')


    auth_header = request.headers.get('Authorization')
    if auth_header:
        access_token = auth_header.split(' ')[1]
    else:
        access_token = 'Invalid Token'

    if access_token:

        for token in BlacklistToken.blacklist_tokens:
            "Check if input access token is blacklisted, if yes, prompt new login"
            if token == access_token:
                responce = make_response(jsonify({'status':'You are already Logged Out, kindly login first'}),400)
                return responce 
          

        """Decode token"""
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            
            try:
                if business_name1 and about1 and location1 and category1:

                    business_name = str(business_name1.strip(' '))
                    location = str(location1.strip(' '))
                    category = str(category1.strip(' '))
                    about = str(about1.strip(' '))
                else:
                    return jsonify({'message': "Fill in the empty fields"}), 400
                
                if business_name and location and category and about:
                    existing = [bus for bus in Business.business_list if business_name == bus.business_name and businessid != bus.businessid]

                    for business in Business.business_list:
                        if businessid == business.businessid:
                            if existing:
                                return jsonify({'message':'That business name is already registered'}), 409

                            business.business_name=business_name
                            business.location=location
                            business.category=category
                            business.about=about 

                             
                            return jsonify({'message':'Business Updated Successfully'}), 200
                          
                    return jsonify({'message':'Business not found'}), 404
                            
                return jsonify({'message':'Fill in the Empty fields'}), 400
                
            except Exception as e:
                return make_response(jsonify({'message': e})), 401

        return make_response(jsonify({'message': 'Invalid token, Login to obtain a new token'})), 401

@bs.route('/api/v1/businesses/<int:businessid>', methods=['DELETE'])
def delete_businesses(businessid):
    """This endpoint removes a business of the given ID from the business list"""
    
    """ Ensure Authorisation"""
    
    auth_header = request.headers.get('Authorization')
    if auth_header:
        access_token = auth_header.split(' ')[1]
    else:
        access_token = 'Invalid Token'

    if access_token:

        for token in BlacklistToken.blacklist_tokens:
            "Check if input access token is blacklisted, if yes, prompt new login"
            if token == access_token:
                responce = make_response(jsonify({'status':'You are already Logged Out, kindly login first'}),400)
                return responce 
          

        """Decode token"""
        user_id = User.decode_token(access_token)

        if not isinstance(user_id, str):
            
            try:
                del_business = [business for business in Business.business_list if businessid == business.businessid]
                if del_business:
                    del_business = del_business[0]
                    
                    """Checks if that ID exists in our business list, if it does, delete"""
                    Business.business_list.remove(del_business)    
                    return jsonify({'message':'Business Deleted Successfully'}), 200
                    
                return jsonify({'message':'No Business with that ID'}), 404

            except Exception as e:
                return make_response(jsonify({'message': e})), 401

        return make_response(jsonify({'message': 'Invalid token, Login to obtain a new token'})), 401